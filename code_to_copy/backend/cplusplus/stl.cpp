

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
