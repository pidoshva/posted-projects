/*
Team Void: UVSim
instructions.cpp
*/
#include <iostream>
#include <climits>
#include "exceptions.h"
#include "instructions.h"
#include "memory.h"
using namespace std;

//I/O Operations

void instructions::read(int operand, Memory& m){
    int input_value;
    cout<<"\nEnter an integer: ";
    if (!(cin >> input_value)) // check if input_value is a valid integer, throw error: not and integer
        throw runtime_error("Error: Invalid input, must be a signed 32-bit integer.");
    m.set_value(operand,input_value);
}

void instructions::write(int operand, Memory& m){
    int output_value = m.get_value(operand);
    cout<<"The value at this location is: "<<output_value<<endl;
}

void instructions::writeChar(int operand, Memory& m){
    int asciiVal = m.get_value(operand);
    char character = char(asciiVal);
    cout<<character<<endl;
}

// LOAD and STORE Operations
 
void instructions::load(int operand, Memory& m) {
    m.A = m.get_value(operand);
}

void instructions::store(int operand, Memory& m) {
    m.set_value(operand, m.A);
}

void instructions::loadval(int operand, Memory& m) {
    m.A = operand;
}

//Arithmetic Operations
    
void instructions::add (int operand, Memory& m) {
    // check if value at memory[operand] is unsigned 32 bit integer, otherwise throw error: invalid math operation
    int pre_op = m.A;
    m.A += m.get_value(operand);
}
    
void instructions::subtract (int operand, Memory& m) {
    // check if value at memory[operand] is an unsigned 32 bit integer, otherwise throw error: invalid math operation
    int pre_op = m.A;
    m.A -= m.get_value(operand);
}

void instructions::divide (int operand, Memory& m) {
    // check if value at memory[operand] is an unsigned 32 bit integer, otherwise throw error: invalid math operation
    int pre_op = m.A;
    if (m.get_value(operand) == 0) { // check memory[operand] for zero, throw error: divide by zero
        throw runtime_error("Error: Divide by zero.");
    }
    m.A /= m.get_value(operand);
}

void instructions::multiply (int operand, Memory& m) {
    // check if value at memory[operand] is an unsigned 32 bit integer, otherwise throw error: invalid math operation
    int pre_op = m.A;
    m.A *= m.get_value(operand);
}

//Branch control operations

void instructions::branch (int operand, Memory& m) {
    m.IC = operand - 1; // decrement before returning so IC is pointing at correct location
}

void instructions::branchneg (int operand, Memory& m) {
    if (m.A < 0) {
        m.IC = operand - 1; // decrement before returning so IC is pointing at correct location
    }
}

void instructions::branchzero (int operand, Memory& m) {
    if (m.A == 0) {
        m.IC = operand - 1; // decrement before returning so IC is pointing at correct location 
    }
}