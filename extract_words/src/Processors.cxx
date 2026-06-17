

#include "../Include/Processors.h"
#if defined(_WIN32)
#include <Windows.h>
#endif

bool isPulaarLetter(char32_t c)
{
    // Define all extra Pulaar letters
    static const std::unordered_set<char32_t> pulaar_extra = {
        U'ɓ', U'ɗ', U'ƴ', U'ŋ', U'ñ',
        U'Ɓ', U'Ɗ', U'Ƴ', U'Ŋ', U'Ñ'};

    // Standard ASCII letters
    if ((c >= U'a' && c <= U'z') || (c >= U'A' && c <= U'Z'))
        return true;

    // Pulaar-specific letters
    if (pulaar_extra.find(c) != pulaar_extra.end())
        return true;

    return false;
}



std::u32string convertToUTF32(const std::string &utf8)
{
#if defined(_WIN32)

    int wlen = MultiByteToWideChar(CP_UTF8, 0, utf8.c_str(), -1, nullptr, 0);
    if (wlen == 0)
        throw std::runtime_error("Invalid UTF-8 input");

    std::wstring wstr(wlen, 0);
    MultiByteToWideChar(CP_UTF8, 0, utf8.c_str(), -1, &wstr[0], wlen);

    std::u32string u32;
    for (wchar_t wc : wstr)
        u32.push_back(static_cast<char32_t>(wc));

    return u32;

#else
    std::u32string u32;
    size_t i = 0;
    while (i < utf8.size())
    {
        uint32_t ch = 0;
        unsigned char c = utf8[i];
        size_t extra_bytes = 0;

        if (c <= 0x7F)
        {
            ch = c;
            extra_bytes = 0;
        }
        else if ((c & 0xE0) == 0xC0)
        {
            ch = c & 0x1F;
            extra_bytes = 1;
        }
        else if ((c & 0xF0) == 0xE0)
        {
            ch = c & 0x0F;
            extra_bytes = 2;
        }
        else if ((c & 0xF8) == 0xF0)
        {
            ch = c & 0x07;
            extra_bytes = 3;
        }
        else
            throw std::runtime_error("Invalid UTF-8 byte sequence");

        if (i + extra_bytes >= utf8.size())
            throw std::runtime_error("Truncated UTF-8 sequence");

        for (size_t j = 1; j <= extra_bytes; ++j)
        {
            unsigned char cc = utf8[i + j];
            if ((cc & 0xC0) != 0x80)
                throw std::runtime_error("Invalid UTF-8 continuation byte");
            ch = (ch << 6) | (cc & 0x3F);
        }

        u32.push_back(ch);
        i += 1 + extra_bytes;
    }

    return u32;
#endif
}

#include <string>
#include <stdexcept>

std::string convertFromUTF32(const std::u32string &u32str)
{
#if defined(_WIN32)
    // Convert UTF-32 -> UTF-16 (wchar_t on Windows)
    std::wstring wstr;
    for (char32_t c : u32str)
        wstr.push_back(static_cast<wchar_t>(c));

    // Then UTF-16 -> UTF-8
    int len = WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), -1, nullptr, 0, nullptr, nullptr);
    if (len == 0)
        throw std::runtime_error("Failed to calculate UTF-8 length");

    std::string utf8(len, 0);
    WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), -1, &utf8[0], len, nullptr, nullptr);

    // Remove null terminator added by WideCharToMultiByte
    if (!utf8.empty() && utf8.back() == '\0')
        utf8.pop_back();

    return utf8;

#else
    // Unix: manual UTF-32 -> UTF-8 encoding
    std::string utf8;
    for (char32_t ch : u32str)
    {
        if (ch <= 0x7F)
        {
            utf8.push_back(static_cast<char>(ch));
        }
        else if (ch <= 0x7FF)
        {
            utf8.push_back(static_cast<char>(0xC0 | ((ch >> 6) & 0x1F)));
            utf8.push_back(static_cast<char>(0x80 | (ch & 0x3F)));
        }
        else if (ch <= 0xFFFF)
        {
            utf8.push_back(static_cast<char>(0xE0 | ((ch >> 12) & 0x0F)));
            utf8.push_back(static_cast<char>(0x80 | ((ch >> 6) & 0x3F)));
            utf8.push_back(static_cast<char>(0x80 | (ch & 0x3F)));
        }
        else if (ch <= 0x10FFFF)
        {
            utf8.push_back(static_cast<char>(0xF0 | ((ch >> 18) & 0x07)));
            utf8.push_back(static_cast<char>(0x80 | ((ch >> 12) & 0x3F)));
            utf8.push_back(static_cast<char>(0x80 | ((ch >> 6) & 0x3F)));
            utf8.push_back(static_cast<char>(0x80 | (ch & 0x3F)));
        }
        else
        {
            throw std::runtime_error("Invalid UTF-32 code point");
        }
    }
    return utf8;
#endif
}

char32_t pulaar_tolower(char32_t c)
{
    if (c >= U'A' && c <= U'Z')
        return c + (U'a' - U'A');

    switch (c)
    {
    case U'Ɓ':
        return U'ɓ';
    case U'Ɗ':
        return U'ɗ';
    case U'Ƴ':
        return U'ƴ';
    case U'Ŋ':
        return U'ŋ';
    case U'Ñ':
        return U'ñ';
    }

    return c;
}


