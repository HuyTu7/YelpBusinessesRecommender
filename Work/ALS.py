from __future__ import print_function

import argparse
import logging
import time

import annoy
import numpy
import pandas
from scipy.sparse import coo_matrix

from implicit.als import AlternatingLeastSquares
from implicit.nearest_neighbours import (BM25Recommender, CosineRecommender,
                                         TFIDFRecommender, bm25_weight)


def read_data(filename):
    data = pandas.read_csv(filename, skiprows = 0, usecols=[2, 3, 4], names=['user', 'business', 'rating'])

    data['user'] = data['user'].astype("category")
    data['business'] = data['business'].astype("category")
    ratings = coo_matrix((data['rating'].astype(float), (data['business'].cat.codes.copy(), data['user'].cat.codes.copy())))

    return data, ratings

#copied from the internet

class AnnoyAlternatingLeastSquares(AlternatingLeastSquares):
    """ A version of the AlternatingLeastSquares model that uses an annoy
    index to calculate similar items. This leads to massive speedups
    when called repeatedly """
    def fit(self, Ciu):
        # train the model
        super(AnnoyAlternatingLeastSquares, self).fit(Ciu)

        # build up an index with all the item_factors
        index = annoy.AnnoyIndex(self.item_factors.shape[1], 'angular')
        for i, row in enumerate(self.item_factors):
            index.add_item(i, row)
        index.build(self.factors / 2)
        self.index = index

    def similar_items(self, businessid, N=10):
        neighbours = self.index.get_nns_by_item(businessid, N)
        return sorted(((other, 1 - self.index.get_distance(businessid, other))
                      for other in neighbours), key=lambda x: -x[1])

def calculate_similar_businesses(input_filename, output_filename, model_name="als", factors=50, regularization=0.01, iterations=15, exact=False, trees=20, use_native=True, dtype=numpy.float64, cg=False):
    logging.debug("Calculating similar businesses. This might take a while")

    # read in the input data file
    logging.debug("reading data from %s", input_filename)
    start = time.time()
    df, ratings = read_data(input_filename)
    logging.debug("read data file in %s", time.time() - start)

    # generate a recommender model based off the input params
    if exact:
        model = AlternatingLeastSquares(factors=factors, regularization=regularization, use_native=use_native, use_cg=cg, dtype=dtype)
    else:
        model = AnnoyAlternatingLeastSquares(factors=factors, regularization=regularization, use_native=use_native, use_cg=cg, dtype=dtype)

    # lets weight these models by bm25weight.
    logging.debug("weighting matrix by bm25_weight")
    ratings = bm25_weight(ratings, K1=100, B=0.8)

    # train the model
    logging.debug("training model %s", model_name)
    start = time.time()
    model.fit(ratings)
    logging.debug("trained model '%s' in %s", model_name, time.time() - start)

    # write out similar businesses by popularity
    logging.debug("calculating top businesses")
    user_count = df.groupby('business').size()
    businesses = dict(enumerate(df['business'].cat.categories))
    to_generate = sorted(list(businesses), key=lambda x: -user_count[x])

    # write out as a TSV of businessid, otherbusinessid, score
    with open(output_filename, "w") as o:
        for businessid in to_generate:
            business = businesses[businessid]
            for other, score in model.similar_items(businessid, 11):
                o.write("%s\t%s\t%s\n" % (business, businesses[other], score))

if __name__ == "__main__":
    calculate_similar_businesses("review.csv", "recommendations.csv")