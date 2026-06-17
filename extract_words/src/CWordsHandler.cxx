
#include "../Include/CWordsHandler.h"
#include <vector>
#include <filesystem>
namespace fs = std::filesystem;


bool CWordsHandler::operator()(int /*line_number*/,
                              int /*word_number*/,
                              std::u32string word)
{
    std::transform(word.begin(), word.end(), word.begin(),
                   [](char32_t c)
                   { return pulaar_tolower(c); });

    words.emplace(word);

    if (++count % 10000 == 0){
        std::cout << "CWordHandler processed " << count << " words." << std::endl;
    }
        word_freq[word]++;
    return true;
}




/**
 * @brief This function stores the extracted words into files(.txt)
 * 
 * @param directory 
 * @return true 
 * @return false 
 */
bool CWordsHandler::store_them(const char* directory){

    std::cout<<"Storing words..."<<std::endl;

    if (!fs::exists(directory) || !fs::is_directory(directory))
    {
        return false;
    }

    /// @brief We could have used constexpr so the compiler __Knows it at compile time__
    const std::size_t MAX_PER_FILE = 10000;
    
    std::size_t word_count = 0;
    std::size_t file_index = 1;

    std::ofstream file;

    /// @brief The lambda uses [&] __to reference what is inside it so the modification is applied to the real object__

    auto open_new_file = [&]() -> bool
    {
        if (file.is_open())
            file.close();

        std::string filename =
            std::string(directory) + "/list_" + std::to_string(file_index++) + ".txt";

        file.open(filename, std::ios::out | std::ios::binary);
        return file.is_open();
    };

    if (!open_new_file())
        return false;

    for (const auto &word : words)
    {

        if (word_count == MAX_PER_FILE)
        {
            word_count = 0;
            if (!open_new_file())
                return false;
        }

        file << convertFromUTF32(word) << '\n';

        ++word_count;
    }

    return true;
}