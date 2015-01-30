#ifndef GENERALOUTPUT     // include guard.
#define GENERALOUTPUT 1

#include <healpix_map.h> // For RandAngInPix function.
#include <alm.h>         // For GeneralOutput function.
#include <xcomplex.h>    // For GeneralOutput function.
#include "ParameterList.hpp"
#include "Utilities.hpp"


/*** Alm's output ***/

// Many alm's in one single table:
void GeneralOutput(Alm<xcomplex <double> > *af, const ParameterList & config, std::string keyword, int **fnz, int Nfields);
// One alm in one table, named with a prefix and the field ID:
void GeneralOutput(const Alm<xcomplex <double> > & a, const ParameterList & config, std::string keyword, int *fnz);
// One alm in one table, names with a keyword:
void GeneralOutput(const Alm<xcomplex <double> > & a, const ParameterList & config, std::string keyword);


/*** Healpix map output ***/

// Prints one single map to FITS file based on a PREFIX and a FIELD ID:
void GeneralOutput(const Healpix_Map<double> & map, const ParameterList & config, std::string keyword, int *fnz);
// Prints a list of maps to a single TEXT file:
void GeneralOutput(Healpix_Map<double> *mapf, const ParameterList & config, std::string keyword, int **fnz, int N1, int N2);
// One set of (Kappa, gamma1, gamma2) maps to one FITS file, named with a prefix and the field ID:
void GeneralOutput(const Healpix_Map<double> & kmap, const Healpix_Map<double> & g1map, 
		   const Healpix_Map<double> & g2map, const ParameterList & config, std::string keyword, int *fnz);
// One set of (Kappa, gamma1, gamma2) maps to one FITS file, named with a keyword:
void GeneralOutput(const Healpix_Map<double> & kmap, const Healpix_Map<double> & g1map, 
		   const Healpix_Map<double> & g2map, const ParameterList & config, std::string keyword);
// One single map to one FITS file, named with a keyword:
void GeneralOutput(const Healpix_Map<double> & map, const ParameterList & config, std::string keyword);
// Prints a list of maps to a many FITS files:
void GeneralOutput(Healpix_Map<double> *mapf, const ParameterList & config, std::string keyword, int **fnz, int Nfields);
#endif
