

#pragma once
#include <unordered_map>
#include <string>
#include <algorithm>
#include <iostream>
#include <set>
#include "Processors.h"


class CWordsHandler
{

private:
    std::unordered_map<std::u32string, int> word_freq;
    int count = 0;
    std::set<std::u32string> words;
public:
    

    /// @brief This is a foncter that populates the wordhouse vector and save is
    /// @param  line_number
    /// @param  word_number
    /// @param  word
    /// @param  wordhouse 
    /// @return boolean

    bool operator()(int line_number,
                    int word_number,
                    std::u32string word);


    inline std::set<std::u32string>& getWords(){return words;}

    bool store_them(const char* directory);

};
