#include<iostream>
#include<vector>
#include<set>
#include<map>
#include<string>
#include<tuple>
using namespace std;

std::set<char> extract_characters(const std::string& regex) {
    std::set<char> characters;
    for (char c : regex) {
        if (c != '(' && c != ')' && c != '|' && c != '*') {
            characters.insert(c);
        }
    }
    return characters;
}

void print_set(set<char>& s){
    cout<<"字母集如下:"<<endl;
    for(auto i:s){
        cout<<i<<" ";
    }
    cout<<endl;
}

std::vector<std::vector<int>> to_transitions(const std::set<char>& alphabeta, int start_state, int end_state){
    std::vector<std::vector<int>> transitions;

    // Initialize the transition matrix with -1, indicating no transition
    for (int i = 0; i <= end_state; ++i) {
        transitions.push_back(std::vector<int>(alphabeta.size(), -1));
    }

    // Define the transitions for the given regular expression
    int current_state = start_state;
    for (char symbol : alphabeta) {
        if (current_state < end_state) {
            transitions[current_state][symbol - 'a'] = current_state + 1;
            current_state++;
        }
    }

    return transitions;
}


int main(){
    string str="(a|b)*abb";

    set<char> alphabeta=extract_characters(str);

    print_set(alphabeta);

    std::vector<std::vector<int>> transitions=to_transitions(alphabeta,0,1);

    for(auto i:transitions){
        for(auto j:i){
            cout<<j<<" ";
        }
        cout<<endl;
    }

    return 0;
}