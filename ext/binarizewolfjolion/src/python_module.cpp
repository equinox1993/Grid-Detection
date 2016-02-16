
#define PY_ARRAY_UNIQUE_SYMBOL pbcvt_ARRAY_API
#include <boost/python.hpp>
#include <pyboostcvconverter/pyboostcvconverter.hpp>
#include "binarizewolfjolion.hpp"
namespace binarizewolfjolion {

	using namespace boost::python;

    PyObject* binarize(PyObject *im, int winx, int winy, double k, double dR) {
        cv::Mat input;
        input = pbcvt::fromNDArrayToMat(im);
        cv::Mat output (input.rows, input.cols, CV_8U);
        binarizewolfjolion::NiblackSauvolaWolfJolion(input, output,
                                                     binarizewolfjolion::NiblackVersion::WOLFJOLION,
                                                     winx, winy, k, dR);
        PyObject* ret = pbcvt::fromMatToNDArray(output);
        return ret;
    }
    
	static void init_ar(){
		Py_Initialize();
	
		import_array();
	}

	BOOST_PYTHON_MODULE(binarizewolfjolion){
		//using namespace XM;
		init_ar();

		//initialize converters
		to_python_converter<cv::Mat,
		pbcvt::matToNDArrayBoostConverter>();
		pbcvt::matFromNDArrayBoostConverter();

		//expose module-level functions
		def("binarize", binarize);
	}

} //end namespace pbcvt
