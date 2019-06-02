/*
* Testing framework for stream algorithms
* Copyright (c) 2013 Lu Wang <coolwanglu@gmail.com>
*/

/*
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/
#ifndef TEST_H__
#define TEST_H__

#include "csv.h"
#include <random>
#include <vector>
#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>

template<class T>

void test(int argc, char ** argv)
{
	// int n = 1;
	for (int k = 0; k < 4; k++) {
		string path = argv[1];
		string data_path = path + "data.csv";
		string eq_path = path + "result/eq.csv";

		// string gkPath = "/home/zwy/Documents/quantile/data/http/" + date + "_101_est_gk.csv";
		// string errPath = "/home/zwy/Documents/quantile/data/http/" + date + "_101_err_gk.csv";
		
		vector<double> v = readcsv(data_path);
		vector<double> eq = readcsv(eq_path);
		// long length = v.size();
		double scale = 1;

		const double eps = 0.01;
		T alg(eps);
		for (auto i : v) {
			alg.feed(i * scale);
			// cout << "feed " << i * 10000 << endl;
		}
		alg.finalize();

		vector<double> result;
		for (double i = 0; i <= 1.01; i += eps) {
			double val = alg.query_for_value(i);
			result.push_back(val);
		}

		cout << result.size() << endl;
		cout << eq.size() << endl;
		cout << "------------------" << endl;

		vector<double> error;
		for(int j = 0; j < eq.size(); j++) {
			double err = abs(result[j] - eq[j]) / eq[j];
			error.push_back(err);	
		}

		// writecsv(gkPath, result);
		// writecsv(errPath, error);
		cout.precision(6);
		cout << "est:" << endl;
		for(int i = 0; i < eq.size(); i++) {
			std::printf("%15.6f", result[i]);
			std::printf("\n");
		}
		cout << endl;
		cout << "err:" << endl;
		for(int i = 0; i < error.size(); i++) {
			std::printf("%15.6f", error[i]);
			std::printf("\n");
		}
		cout << endl;
	}
}

#endif //TEST_H__
