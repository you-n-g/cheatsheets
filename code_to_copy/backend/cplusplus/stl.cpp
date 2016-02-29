

// common
using namespace std;

auto f = [](int x) -> int {return x;} // 返回值可以为空，然后它会自动判定返回值的类型。 

// vector
#include<vector>
vector<int> nums:
int index;

for (vector<int>::iterator it = nums.begin(); it != nums.end(); it++) {
    index = it - nums.begin(); // this will not compile if change it to a list.
    index = std::distance(vec.begin(), it); // this will change the algorithm to O(n^2)
}
nums.push_back(STH);

cout << vector<int>({1,2}).back() << endl;  // 使用匿名对象


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
equal_bound(v.begin(), v.end(), VAL); // 直接求出等于VAL的阈值，返回upper_bound和 lower_bound

sort(v.begin(), v.end()); // 有快排的效率

v.erase(unique(v.begin(), v.end()), v.end()); // 可以把数组中连续的重复数字都去除，数值网前移动，最后用erase 删除掉其他数值

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

// sub striing
str.substr(INDEX, LENGTH);

// find sub string
std::size_t found = str.find(str2);
if (found != std::string::npos) // 如果找到了
// 一般来说， 如果返回值是iterator， 那找没找到看 object.end()； 如果返回值是位置， 找没找到看 class::npos;


// useful numbers
#include <climits>
INT_MAX // (2147483647) 
INT_MIN // (-2147483648)

// 对象有哪些方法 http://www.cplusplus.com/reference/string/string/





// iostream 输出格式设置
// 设置小数格式
cout.precision(5);
cout << fixed << f << endl;
cout << scientific << f << endl;

// 整数
cout.width(10);
cout.fill('0');
cout << dec << 20 << endl;
