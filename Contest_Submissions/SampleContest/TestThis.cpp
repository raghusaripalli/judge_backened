#include<iostream>
#include<set>
//#include<bits/stdc++.h>
using namespace::std;

#define sz(a) (int)a.size()

int main(){
      int N;
      int x;
      cin >> N;
      set<int> MySet;
     // N = N/0;
      for(int i=0;i<N;i++){
      		
            cin >> x;
            MySet.insert(x);
      }
      cout << MySet.size() << endl;
     // while(true);
      return 0;
}
