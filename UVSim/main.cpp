/*
Team Void: UVSim
main.cpp
*/
#include "memory.h"
#include "vm.h"
#include <iostream>
#include <fstream>
#include <cstdio>
#include <limits>
#include <string>
#include <vector>
using namespace std;

vector<int> getUserProgramInput(Memory& m);
const string MEMORY_DUMP_TO_FILE = "memory.txt";
const string INSTRUCTION_WRITE_FILE = "instructions.txt";
string INSTRUCTION_READ_FILE = "instructions.txt";

void runProgramInMemory(Memory& m);
int promptMenu(string question, string options[], int numOptions);
void mainMenu();
void demoMenu();
void runProgram(bool instructions_write_flag, bool instructions_read_flag, bool memory_output_flag);
void write_instructions_to_file(vector<int> v, string filename);
void memoryOutToFile(Memory& m);
void loadFromFile(Memory& m);
void printLogo();
void runDemo(string filePath);
void about();

void printLogo() {
    cout <<"\033[32;1;4m██╗   ██╗██╗   ██╗███████╗██╗███╗   ███╗\033[0m"<<endl;
    cout <<"\033[32;1;4m██║   ██║██║   ██║██╔════╝██║████╗ ████║\033[0m"<<endl;
    cout <<"\033[32;1;4m██║   ██║██║   ██║███████╗██║██╔████╔██║\033[0m"<<endl;
    cout <<"\033[32;1;4m██║   ██║╚██╗ ██╔╝╚════██║██║██║╚██╔╝██║\033[0m"<<endl;
    cout <<"\033[32;1;4m╚██████╔╝ ╚████╔╝ ███████║██║██║ ╚═╝ ██║\033[0m"<<endl;
    cout <<"\033[32;1;4m ╚═════╝   ╚═══╝  ╚══════╝╚═╝╚═╝     ╚═╝\033[0m"<<endl;
}

int main() {
    printLogo();
    mainMenu();
    return 0;
}

void write_instructions_to_file(vector<int> v, string file_name = INSTRUCTION_WRITE_FILE) {//for user instructions
    ofstream ofs;
    ofs.open(file_name, fstream::trunc);
    for (const int& i : v) // iterate through vector putting each item in file
        ofs << i << endl;
    ofs.close();
}

void memoryOutToFile(Memory& m) {//for memory
  m.dumpMemory(MEMORY_DUMP_TO_FILE);
}

void mainMenu(){
    string options[6] = { "Run Regular Program", "Run Program and Save", "Run Program from Load", "Demos", "Quit", "About"};
    int choice = promptMenu("Main Menu", options, sizeof(options)/sizeof(options[0]));
    bool instructions_write_flag = false;
    bool instructions_read_flag = false;
    bool memory_output_flag = false;
    switch(choice){
      case 1:
        runProgram(instructions_write_flag, instructions_read_flag, memory_output_flag);
        break;
      case 2:// write to file
        instructions_write_flag = true;
        memory_output_flag = true;
        runProgram(instructions_write_flag, instructions_read_flag, memory_output_flag);
        cout << "Saving..." << endl;
        break;
      case 3:
        cout << "Loading..." << endl;
        instructions_read_flag = true;
        runProgram(instructions_write_flag, instructions_read_flag, memory_output_flag);
        break;
      case 4:
        demoMenu();
        break;
      case 5:
        cout << "Exiting Program" << endl;
        return;
        break;
      case 6:
        about();
        mainMenu();
        return;
        break;
    }
    mainMenu();//to go back to this menu after option execution
}

void demoMenu() {
    string options[4] = { "Fibonacci", "Is Prime", "Demo Name", "To Main Menu" };

    int choice = promptMenu("Demo Menu", options, sizeof(options) / sizeof(options[0]));
    switch (choice) {
    case 1:
        runDemo("demos/fibonacci.txt");
        break;
    case 2:
        runDemo("demos/is_prime.txt");
        break;
    case 3:
        runDemo("demos/is_prime.txt");
        break;
    case 4://to Main Menu
        return;
        break;
    }
    demoMenu();//to go back to this menu after option execution
}

void runDemo(string filePath){
        INSTRUCTION_READ_FILE = filePath;
        runProgram(false, true, false);
        INSTRUCTION_READ_FILE = "instructions.txt";
}

void runProgram(bool instructions_write_flag, bool instructions_read_flag, bool memory_output_flag){

    //set up memory
    Memory m;
    for (int i = 0; i < m.capacity; i++){//initialize memory to be all zeros
        m.set_value(i,0);
    }

    //user input
    vector<int> input;
    if(instructions_read_flag){
      loadFromFile(m);
    } else {
      input = getUserProgramInput(m);
    }

    // call write_instructions_to_file with vector passed back by getUserProgramInput in variable, check flag
    if(instructions_write_flag){
      write_instructions_to_file(input);
    }

    VM(m);
    m.dumpMemory("");//arg is blank file path

    if(memory_output_flag){
      memoryOutToFile(m);
    }
}

void runProgramInMemory(Memory& m){
    //run program in memory
    cout<<"*** Program execution begins ***"<<endl;
    VM(m);
    m.dumpMemory("");
    memoryOutToFile(m);
}

// Loading saved data from a file to the Memory
void loadFromFile(Memory& m){

  ifstream file;
    file.open(INSTRUCTION_READ_FILE);

    if (file.is_open()) {
        int i = 0;
        int element;

        while (file >> element) {
          if (element == -99999) { // Exit condition
              m.last_address = i;
              break;
          }
            m.set_value(i++,element); // Reading instructions to the memory one by one

    }
  }
  cout<<"\n*** Program loading complete ***"<<endl;
}

vector<int> getUserProgramInput(Memory& m){
    cout << "\n*** Welcome to UVSim! ***" << endl;
    cout << "*** Please enter your program one instruction ***" << endl;
    cout << "*** ( or data word ) at a time into the input ***" << endl;
    cout << "*** text field.  The line number and a quest- ***" << endl;
    cout << "*** ion mark will display.  Type the instruc- ***" << endl;
    cout << "*** ion for that line. Enter -99999 to compl- ***" << endl;
    cout << "*** plete entering your program and run.      ***\n" << endl;

    vector<int> write_vector;
    int input;

    for (int i = 0; i < m.capacity; i++) {

        if (i < 10)
            cout << "0" << i << ": ";
        else
            cout << i << ": ";

        cin >> input;

        if (input == -99999) { // Exit condition
            write_vector.push_back(input);
            m.last_address = i;
            break;
        }
        if (input < 10000 || input > 99999) { // Not storing in memory if out of range
            i--;
            cout << "ML command is the incorrect length, please input a two digit opcode and three digit memory location.\n";
            cin.clear();
            cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            continue;
        }
        write_vector.push_back(input);
        m.set_value(i, input);
    }

    cout<<"\n*** Program loading complete ***"<<endl;
    return write_vector; // default to TEMP_FILE, can use filename given by user
}

int promptMenu(string question, string options[], int numOptions){
    cout << "\n\n" << question << "\n";
    for(int i = 0; i < numOptions; i++){
        cout << i+1 << "\t" << options[i] << "\n";
    }

    int input;
    //get and validate user input
    cout<<"Enter Choice: ";
    cin>>input;
    while(1){
      if(cin.fail() || input < 1 || input > numOptions){
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(),'\n');
        cout<<"Please enter a valid input"<<endl;
        cin>>input;
      } else {
        break;
      }
    }

    return input;
}

void about(){
  cout<<"\nLIST OF OPERATIONS: "<<endl;
  cout<<"\tREAD       - 10 --- Reads a keyboard into the specific location in memory."<<endl;
  cout<<"\tWRITE      - 11 --- Write a word from the specific location in memory to screen."<<endl;
  cout<<"\tWRITECHAR  - 12 --- Writes a character from the specific location in memory to screen, translating the value as ascii to character."<<endl;
  cout<<"\tLOAD       - 20 --- Load a word from a specific location memory into the accumulator."<<endl;
  cout<<"\tSTORE      - 21 --- Store a word from the accumulator into a specific location in memory."<<endl;
  cout<<"\tLOADVAL    - 22 --- Loads a 3 digit number into the accumulator."<<endl;
  cout<<"\tADD        - 30 --- Add a word from a specific location in memory to the word in the accumulator and leave the result in <<accumulator."<<endl;
  cout<<"\tSUBTRACT   - 31 --- Subtract a word from a specific location in memory from the word in the accumulator and leave the result in accumulator."<<endl;
  cout<<"\tDIVIDE     - 32 --- Divide the word in the accumulator by a word from a specific location in memory and leave the result in accumulator."<<endl;
  cout<<"\tMULTIPLY   - 33 --- Multiply a word from a specific location in memory to the word in the accumulator and leave the result in accumulator."<<endl;
  cout<<"\tBRANCH     - 40 --- Branch to a specific location in memory."<<endl;
  cout<<"\tBRANCHNEG  - 41 --- Branch to a specific location in memory if the accumulator is negative."<<endl;
  cout<<"\tBRANCHZERO - 42 --- Branch to a specific location in memory if the accumulator is zero."<<endl;
  cout<<"\tHALT       - 43 --- Pause the program."<<endl;
  cout <<"\nFor more information please visit: https://github.com/QualityError/TeamVoid-UVSim#readme"<< endl;
}
