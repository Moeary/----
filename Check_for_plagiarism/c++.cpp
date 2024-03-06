#include <iostream>
#include <fstream>
#include <unordered_set>
#include <vector>
#include <sstream> // Add this line
#include <regex>
using namespace std;

// 计算两个字符串的重复率
double compute_similarity(const string& str1, const string& str2, int n) {
    // 将字符串拆分成单词
    vector<string> words1, words2;
    istringstream iss1(str1);
    istringstream iss2(str2);
    string word;
    while (iss1 >> word) {
        words1.push_back(word);
    }
    while (iss2 >> word) {
        words2.push_back(word);
    }

    // 创建哈希表来存储单词
    unordered_set<string> hash_set;
    for (const string& word : words1) {
        hash_set.insert(word);
    }

    // 计算重复的单词数量
    int num_repeats = 0;
    for (const string& word : words2) {
        if (hash_set.find(word) != hash_set.end()) {
            num_repeats++;
        }
    }

    // 计算重复率
    double similarity = static_cast<double>(num_repeats) / max(words1.size(), words2.size());

    return similarity;
}

// 读取文件并预处理内容
string read_file(const string& filename) {
    ifstream file(filename);
    stringstream buffer;
    buffer << file.rdbuf();
    file.close();

    string content = buffer.str();

    // Remove single line comments
    std::regex singleLineCommentRegex("//.*");
    content = std::regex_replace(content, singleLineCommentRegex, "");

    // Remove multi-line comments
    std::regex multiLineCommentRegex("/\\*.*?\\*/");
    content = std::regex_replace(content, multiLineCommentRegex, "");

    return content;
}
// 从命令行获取用户输入
#include <cstring>

int main(int argc, char* argv[]) {
    int n;
    string filename1, filename2;

    // Parse command line arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-n") == 0) {
            n = atoi(argv[++i]);
        } else if (strcmp(argv[i], "-file1") == 0) {
            filename1 = argv[++i];
        } else if (strcmp(argv[i], "-file2") == 0) {
            filename2 = argv[++i];
        }
    }

    // 读取两个文件的内容
    string content1 = read_file(filename1);
    string content2 = read_file(filename2);

    // 计算两个文件的重复率
    double similarity = compute_similarity(content1, content2, n);

    // 显示重复率
    cout << "The similarity between the two files is: " << similarity << endl;

    return 0;
}