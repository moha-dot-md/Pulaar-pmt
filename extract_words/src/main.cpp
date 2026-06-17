#include <cstdlib>
#include <iostream>
#include "../Include/Fileshandler.h"
#include "../Include/Processors.h"
#include "../Include/CWordsHandler.h"
#include<vector>


std::vector<std::string> files;

static void gather_files(const std::string filename) {
    files.push_back(filename);
}


static void extract_words(CWordsHandler& handler, std::vector<std::string>& files) {
    std::cout<<"Extracting words"<<std::endl;
    for (auto& name : files )
        ExtractWordsPulaar(name.c_str(), handler);

}



int main(){

    IterOnDir("../inputs",gather_files);
    CWordsHandler handler;
    extract_words(handler, files);
    std::cout<<"Extracted "<<handler.getWords().size()<<std::endl;
    
    handler.store_them("../outputs");


    return (EXIT_SUCCESS);
}