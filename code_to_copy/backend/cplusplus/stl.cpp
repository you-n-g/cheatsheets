

// common
using namespace std;


// vector
#include<vector>
vector<int> nums:
int index;

for (vector<int>::iterator it = nums.begin(); it != nums.end(); it++) {
    index = it - nums.begin(); // this will not compile if change it to a list.
    index = std::distance(vec.begin(), it); // this will change the algorithm to O(n^2)
}
nums.push_back(STH);


// map
#include<map>
map<int, int> mymap;
map<int, int>::iterator mapit;
mapit = mymap.find(STH);
if (mapit != mymap.end()) { // means find something
    mapit->second;
}
mymap[STH] = OTHER_THING; // return a referance. if it doesn't exist, will insert a new element with zeroed value????

mymap.erase(VAL);


// set
#include <set>
set<long long> s;
s.clear();
s.insert(VAL);
s.size();
s.erase(VAL);

// algorithm
#include <algorithm> 
max(VALA, VALB);
min(VALA, VALB);

lower_bound(v.begin(), v.end(), VAL); // first iterator with val >= VAL, otherwith return the position that means v.end()
upper_bound(v.begin(), v.end(), VAL); // first iterator with val > VAL,


//string
#include<string>
str = to_string(INT|FLOAT);

// stoi是C++11支持的标准，  必须加上 -std=c++11 才行
std::string::size_type sz;
int I_DEC = stoi(STR_DEC, &sz, 10);

// 这个版本不需要 C++11的支持
#include<stdlib.h>
INT = atoi(STRING_OBJ.c_str());


// 如何split string, 以','为例
#include<string>
#include<iostream>
#include<sstream> // for stringstream
string s, item;
cin >> s;
stringstream ss(s);
while (getline(ss, item, ',')) {
    cout << item << endl;
}


// useful numbers
#include <climits>
INT_MAX // (2147483647) 
INT_MIN // (-2147483648)

