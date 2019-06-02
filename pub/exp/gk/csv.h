#include<string>
#include <vector>
#include <iostream>
#include <fstream>

using namespace std;

vector<double> readcsv(string path) {
	ifstream in(path);
	string line;
	vector<double> data;
	if (in) {
		while (getline(in, line)) {
			data.push_back(atof(line.c_str()));
		}
	}
	else {
		cout << "no such file" << endl;
	}
	return data;
}

void writecsv(string path, vector<double> data) {
	ofstream out(path);
	if (out) {
		for (auto i: data) {
			out << i<<endl;
		}
	}
}