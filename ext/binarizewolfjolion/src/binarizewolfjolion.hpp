/**************************************************************
 * Binarization with several methods
 * (0) Niblacks method
 * (1) Sauvola & Co.
 *     ICDAR 1997, pp 147-152
 * (2) by myself - Christian Wolf
 *     Research notebook 19.4.2001, page 129
 * (3) by myself - Christian Wolf
 *     20.4.2007
 *
 * See also:
 * Research notebook 24.4.2001, page 132 (Calculation of s)
 **************************************************************/

#ifndef binarizewolfjolion_hpp
#define binarizewolfjolion_hpp

#include <cv.hpp>
#include <highgui.h>
#include <stdio.h>

using namespace std;
using namespace cv;

namespace binarizewolfjolion {
    enum NiblackVersion
    {
        NIBLACK=0,
        SAUVOLA,
        WOLFJOLION,
    };
    
    void NiblackSauvolaWolfJolion (Mat &im, Mat &output, NiblackVersion version,
                                   int winx, int winy, double k, double dR);
    
}

#endif /* binarizewolfjolion_hpp */