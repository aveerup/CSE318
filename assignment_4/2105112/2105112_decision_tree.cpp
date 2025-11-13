#include<bits/stdc++.h>
using namespace std;

void split_string(string &line, vector<string> &words){
  string word = "";
  for(int i = 0; i<line.length(); i++){
    if(line[i] == ','){
      words.push_back(word);
      word = "";
    }else if(line[i] != ' '){
      word += line[i];
    }
  }

  if(!word.empty()){
    words.push_back(word);
  }
}

vector<string> attributes;

void make_training_and_test_data(string file_path){
  ifstream fin(file_path);

  ofstream train_data_file("./CSE 318 Offline 4/Datasets/training.txt");
  ofstream test_data_file("./CSE 318 Offline 4/Datasets/test.txt");

  string line;
  int total_line_no = 0;
  int line_no = 0;
  while(getline(fin, line)){
    total_line_no++;
  }

  fin.clear();
  fin.seekg(0, ios::beg);
  
  random_device rd;                         
  mt19937 gen(rd()); 
//   mt19937 gen(42);                       
  uniform_int_distribution<> dist(0, 4);   

  int randomNum = dist(gen);
  while(getline(fin, line)){
    if(line_no == 0 ){
      train_data_file<<line<<endl;
      test_data_file<<line<<endl;

      attributes.clear();
      split_string(line, attributes);
    }else{
      
      if(line_no%5 == randomNum){
        test_data_file<<line<<endl;
      }else{
        train_data_file<<line<<endl;
      }
      
      if(line_no != 0 && line_no%5 == 0){
        randomNum = dist(gen);
      }
      
    }

    line_no++;
  }

  fin.close();
  train_data_file.close();
  test_data_file.close();
}

bool is_numeric(string word){
    int point = 0;
    for(int i = 0; i<word.length(); i++){
        
        if(word[i] == '.'){
            if(point == 0){
                point = 1;
                continue;
            }else{
                return false;
            }
        }

        if(word[i] >= '0' && word[i] <= '9'){
            continue;
        }else{
            return false;
        }
    }

    return true;
}

void categorize_numerical_data(vector<vector<string>> &data, vector<double> *partitions){
    for(int i = 0; i < data[0].size(); i++){
        if(is_numeric(data[0][i])){
            vector<double> numeric_attr_values;
            for(int j = 0; j < data.size(); j++){
                numeric_attr_values.push_back(stod(data[j][i]));
            }
            
            sort(numeric_attr_values.begin(), numeric_attr_values.end());

            if(partitions->size() == 0){
                double Q1 = numeric_attr_values[1*numeric_attr_values.size()/4];
                double Q2 = numeric_attr_values[2*numeric_attr_values.size()/4];
                double Q3 = numeric_attr_values[3*numeric_attr_values.size()/4];

                partitions->push_back(Q1);
                partitions->push_back(Q2);
                partitions->push_back(Q3);
            }

            for(int j = 0; j < data.size(); j++){
                if((*partitions)[0] > stod(data[j][i])){
                    data[j][i] = "q0";
                }else if((*partitions)[0] <= stod(data[j][i]) && stod(data[j][i]) < (*partitions)[1]){
                    data[j][i] = "q1";
                }else if((*partitions)[1] <= stod(data[j][i]) && stod(data[j][i]) < (*partitions)[2]){
                    data[j][i] = "q2";
                }else{
                    data[j][i] = "q3";
                }
            }
        }
    }
}

vector<vector<string>> load_data(string file_path){
  ifstream fin(file_path);
  string line;
  int line_no = 0;
  vector<vector<string>> data;

  while(getline(fin, line)){
    if(line_no == 0){
      line_no++;
      continue;
    }else{
      vector<string> row_data;
      split_string(line, row_data);
      if(!row_data.empty()){  
        data.push_back(row_data);
      }
    }
    line_no++;
  }

  fin.close();
  return data;
}

struct Node {
  string attribute;
  string value;
  string prediction;
  bool isLeaf;
  map<string, Node*> children;
  
  Node(){
    this->isLeaf = false;
  }
  
  ~Node(){
    for(auto& child : children){
      delete child.second;
    }
    children.clear();
  }
};

class DecisionTree {
  private:
    Node* root;
    vector<string> attributes;
    string criterion;
    int maxDepth = 0;
    int nodeCount = 0;
    int realDepth = 0;
    
    double calculate_entropy(const vector<vector<string>>& data, int classIndex) {
        if (data.empty()) return 0.0;
        
        map<string, int> classCounts;
        for (const auto& row : data) {
            if(classIndex < row.size()){
            classCounts[row[classIndex]]++;
            }
        }
        
        double entropy = 0.0;
        int total = data.size();
        for (const auto& pair : classCounts) {
            double p = (double)pair.second / total;
            entropy -= p * log2(p);
        }

        return entropy;
    }
    
    double calculate_information_gain(const vector<vector<string>>& data, int attrIndex, int classIndex) {
        double totalEntropy = calculate_entropy(data, classIndex);
        
        map<string, vector<vector<string>>> subsets;
        for (const auto& row : data) {
            if(attrIndex < row.size()){
            subsets[row[attrIndex]].push_back(row);
            }
        }
        
        double weightedEntropy = 0.0;
        for (const auto& subset : subsets) {
            double weight = (double)subset.second.size() / data.size();
            weightedEntropy += weight * calculate_entropy(subset.second, classIndex);
        }
        
        return totalEntropy - weightedEntropy;
    }
    
    double calculate_intrinsic_value(const vector<vector<string>>& data, int attrIndex) {
        map<string, int> valueCounts;
        for (const auto& row : data) {
            if(attrIndex < row.size()){
            valueCounts[row[attrIndex]]++;
            }
        }
        
        double iv = 0.0;
        int total = data.size();
        for (const auto& pair : valueCounts) {
            double p = (double)pair.second / total;
            iv -= p * log2(p);
        }

        return iv;
    }
    
    double calculate_nwig(const vector<vector<string>>& data, int attrIndex, int classIndex) {
        double ig = calculate_information_gain(data, attrIndex, classIndex);
        
        set<string> uniqueValues;
        for (const auto& row : data) {
            if(attrIndex < row.size()){
            uniqueValues.insert(row[attrIndex]);
            }
        }
        int k = uniqueValues.size();
        int dataSize = data.size();
        
        if (k <= 1) return 0.0;
        
        double nwig = (ig / log2(k + 1)) * (1.0 - (double)(k - 1) / dataSize);
        return nwig;
    }
    
    int get_best_attribute(const vector<vector<string>>& data, const vector<int>& availableAttrs, int classIndex) {
        int bestAttr = -1;
        double bestScore = -1.0;
        
        for (int attr : availableAttrs) {
            double score = 0.0;
            
            if (criterion == "IG") {
                score = calculate_information_gain(data, attr, classIndex);
            } else if (criterion == "IGR") {
                double ig = calculate_information_gain(data, attr, classIndex);
                double iv = calculate_intrinsic_value(data, attr);
                score = (iv > 0) ? ig / iv : 0.0;
            } else if (criterion == "NWIG") {
                score = calculate_nwig(data, attr, classIndex);
            }
            
            if (score > bestScore) {
                bestScore = score;
                bestAttr = attr;
            }
        }
        
        return bestAttr;
    }
    
    string get_majority_class(const vector<vector<string>>& data, int classIndex) {
        if(data.empty()) return "unknown";
        
        map<string, int> classCounts;
        for (const auto& row : data) {
            if(classIndex < row.size()){
            classCounts[row[classIndex]]++;
            }
        }
        
        string majorityClass = "unknown";
        int maxCount = 0;
        for (const auto& pair : classCounts) {
            if (pair.second > maxCount) {
                maxCount = pair.second;
                majorityClass = pair.first;
            }
        }
        return majorityClass;
    }
    
    bool is_pure(const vector<vector<string>>& data, int classIndex) {
        if (data.empty()) return true;
        
        string firstClass = "";
        for (const auto& row : data) {
            if(classIndex < row.size()){
                if(firstClass.empty()){
                    firstClass = row[classIndex];
                } else if(row[classIndex] != firstClass){
                    return false;
                }
            }
        }
        return true;
    }
    
    Node* build_tree(const vector<vector<string>>& data, vector<int> availableAttrs, int depth, int classIndex) {
        Node* node = new Node();
        nodeCount++;
        realDepth++;
        
        if (data.empty()) {
            node->isLeaf = true;
            node->prediction = "unknown";
            return node;
        }
        
        if (is_pure(data, classIndex) || availableAttrs.empty() || (maxDepth > 0 && depth >= maxDepth)) {
            node->isLeaf = true;
            node->prediction = get_majority_class(data, classIndex);
            return node;
        }
        
        int bestAttr = get_best_attribute(data, availableAttrs, classIndex);
        if (bestAttr == -1) {
            node->isLeaf = true;
            node->prediction = get_majority_class(data, classIndex);
            return node;
        }
        
        node->attribute = attributes[bestAttr];
        
        vector<int> newAvailableAttrs;
        for (int attr : availableAttrs) {
            if (attr != bestAttr) {
                newAvailableAttrs.push_back(attr);
            }
        }
        
        map<string, vector<vector<string>>> subsets;
        for (const auto& row : data) {
            if(bestAttr < row.size()){
                subsets[row[bestAttr]].push_back(row);
            }
        }
        
        int currDepth = realDepth;
        int currMaxDepth = realDepth;
        for (const auto& subset : subsets) {
            
            if(realDepth > currMaxDepth)
                currMaxDepth = realDepth;
            realDepth  = currDepth;

            Node* child = build_tree(subset.second, newAvailableAttrs, depth + 1, classIndex);
            child->value = subset.first;
            node->children[subset.first] = child;
        }
        
        return node;
    }
    
    string predict(Node* node, const vector<string>& instance) {
        if (node->isLeaf) {
            // cout<<1.4<<endl;
            return node->prediction;
        }
        
        string attrValue = "";
        for (int i = 0; i < attributes.size(); i++) {
            if (attributes[i] == node->attribute && i < instance.size()) {
                attrValue = instance[i];
                break;
            }
        }
        
        if (node->children.find(attrValue) != node->children.end()) {
            return predict(node->children[attrValue], instance);
        } else {
            // cout<<attrValue<<endl;
            return get_majority_class_from_node(node);
            return "";
        }
    }
    
    string get_majority_class_from_node(Node* node) {

        map<string, int> classCounts;
        collect_leaf_predictions(node, classCounts);
        
        string majorityClass = "unknown";
        int maxCount = 0;
        for (const auto& pair : classCounts) {
            if (pair.second > maxCount) {
                maxCount = pair.second;
                majorityClass = pair.first;
            }
        }
        
        return majorityClass;
    }
    
    void collect_leaf_predictions(Node* node, map<string, int>& classCounts) {
        if (node->isLeaf) {
            classCounts[node->prediction]++;
        } else {
            for (const auto& child : node->children) {
                collect_leaf_predictions(child.second, classCounts);
            }
        }
    }
    
public:
    DecisionTree(string crit, int max_depth){
        this->criterion = crit;
        this->maxDepth = max_depth;
        this->root = NULL;
    }
    
    ~DecisionTree() {
        if (root != NULL) {
            delete root;
        }
    }
    
    void train(const vector<vector<string>>& data, const vector<string>& attrs) {
        if (root != NULL) {
            delete root;
            root = NULL;
        }
        
        attributes = attrs;
        vector<int> availableAttrs;
        for (int i = 0; i < attributes.size() - 1; i++) {
            availableAttrs.push_back(i);
        }
        
        int classIndex = attributes.size() - 1;
        root = build_tree(data, availableAttrs, 0, classIndex);
    }
    
    string predict(const vector<string>& instance) {
        if (root == NULL) 
            return "unknown";
        
        return predict(root, instance);
    }
    
    double evaluate(const vector<vector<string>>& testData) {
        if (testData.empty())
            return 0.0;
        
        int correct = 0;
        for (const auto& row : testData) {
            string predicted = predict(row);
            string actual = row[row.size() - 1];
            if (predicted == actual) {
                correct++;
            }
        }
        
        return correct / (double)testData.size();
    }
    
    pair<int, int> get_tree_stats() {
        return {nodeCount, realDepth - 1};
    }
};

int main(int argc, char* argv[]) {
  if (argc != 3) {
      cout << "Usage: " << argv[0] << " <criterion> <maxDepth>" << endl;
      cout << "Criterion: IG, IGR, or NWIG" << endl;
      cout << "MaxDepth: 0 for no pruning, positive integer for depth limit" << endl;
      return 1;
  }
  
  string criterion = argv[1];
  int maxDepth = stoi(argv[2]);
  
  if (criterion != "IG" && criterion != "IGR" && criterion != "NWIG") {
      cout << "Invalid criterion. Use IG, IGR, or NWIG." << endl;
      return 1;
  }
  
  vector<double> accuracies;
  vector<pair<int, int>> tree_stats;
  
  cout << "Running experiments with " << criterion << " criterion and max depth " << maxDepth << "..." << endl;
  
  for (int run = 0; run < 20; run++) {
      cout << "Run " << (run + 1) << "/20" << endl;
      
      make_training_and_test_data("./CSE 318 Offline 4/Datasets/adult.data");
    //   make_training_and_test_data("./CSE 318 Offline 4/Datasets/Iris.csv");
      
      vector<vector<string>> trainData = load_data("./CSE 318 Offline 4/Datasets/training.txt");
      vector<vector<string>> testData = load_data("./CSE 318 Offline 4/Datasets/test.txt");
      
      if(trainData.empty() || testData.empty()) {
          cout << "training/testing data load failed" << endl;
          continue;
      }

      vector<double> partitions;
      categorize_numerical_data(trainData, &partitions);
      categorize_numerical_data(testData, &partitions);
      
      DecisionTree tree(criterion, maxDepth);
      tree.train(trainData, attributes);
      
      double accuracy = tree.evaluate(testData);
      accuracies.push_back(accuracy);
      
      if (run == 0) {
          auto stats = tree.get_tree_stats();
          tree_stats.push_back(stats);
          cout << "Tree stats: " << stats.first << " nodes, depth " << stats.second << endl;
      }
      
      cout << "Accuracy: " << accuracy * 100 << "%" << endl;
  }
  
  if(accuracies.empty()) {
      cout << "No valid runs completed." << endl;
      return 1;
  }
  
  double avgAccuracy = 0.0;
  for (double acc : accuracies) {
      avgAccuracy += acc;
  }
  avgAccuracy /= accuracies.size();
  
  cout << endl << "Criterion: " << criterion << endl;
  cout << "Max Depth: " << maxDepth << endl;
  cout << "Average Accuracy: " << avgAccuracy * 100 << "%" << endl;

  int nodes = 0;
  if (!tree_stats.empty()) {
    cout << "Tree Statistics after first run: " << tree_stats[0].first << " nodes, depth " << tree_stats[0].second << endl<<endl;
    nodes = tree_stats[0].first;
  }

  ofstream out_result("./plot_data.txt", ios::app);
  out_result << criterion << ", " << maxDepth << ", " << avgAccuracy << ", " << nodes << endl;
  
  out_result.close();
  
  return 0;
}