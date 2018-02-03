/**
 *-----------------------------------------------------------------------------
 * Title      : Hub Hub
 * ----------------------------------------------------------------------------
 * File       : Hub.cpp
 * Author     : Ryan Herbst, rherbst@slac.stanford.edu
 * Created    : 2016-09-20
 * Last update: 2016-09-20
 * ----------------------------------------------------------------------------
 * Description:
 * A memory interface hub. Accepts requests from multiple masters and forwards
 * them to a downstream slave. Address is updated along the way. Includes support
 * for modification callbacks.
 * ----------------------------------------------------------------------------
 * This file is part of the rogue software platform. It is subject to 
 * the license terms in the LICENSE.txt file found in the top-level directory 
 * of this distribution and at: 
 *    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html. 
 * No part of the rogue software platform, including this file, may be 
 * copied, modified, propagated, or distributed except according to the terms 
 * contained in the LICENSE.txt file.
 * ----------------------------------------------------------------------------
**/
#include <rogue/interfaces/memory/Hub.h>
#include <rogue/GilRelease.h>
#include <rogue/ScopedGil.h>
#include <boost/make_shared.hpp>
#include <boost/python.hpp>

namespace rim = rogue::interfaces::memory;
namespace bp  = boost::python;

//! Create a block, class creator
rim::HubPtr rim::Hub::create (uint64_t offset) {
   rim::HubPtr b = boost::make_shared<rim::Hub>(offset);
   return(b);
}

//! Create an block
rim::Hub::Hub(uint64_t offset) : Master (), Slave(0,0) { 
   offset_ = offset;
}

//! Destroy a block
rim::Hub::~Hub() { }

//! Get offset
uint64_t rim::Hub::getOffset() {
   return offset_;
}

//! Return min access size to requesting master
uint32_t rim::Hub::doMinAccess() {
   return(reqMinAccess());
}

//! Return max access size to requesting master
uint32_t rim::Hub::doMaxAccess() {
   return(reqMaxAccess());
}

//! Return offset
uint64_t rim::Hub::doAddress() {
   return(reqAddress() | offset_);
}

//! Post a transaction. Master will call this method with the access attributes.
void rim::Hub::doTransaction(uint32_t id, boost::shared_ptr<rogue::interfaces::memory::Master> master,
                             uint64_t address, uint32_t size, uint32_t type) {
   uint64_t outAddress;

   // Adjust address
   outAddress = offset_ | address;

   // Forward transaction
   getSlave()->doTransaction(id,master,outAddress,size,type);
}

void rim::Hub::setup_python() {

   bp::class_<rim::HubWrap, rim::HubWrapPtr, bp::bases<rim::Master,rim::Slave>, boost::noncopyable>("Hub",bp::init<uint64_t>())
      .def("create", &rim::Hub::create)
      .staticmethod("create")
       .def("_getAddress",    &rim::Hub::doAddress,     &rim::HubWrap::defDoAddress)
       .def("_getOffset",     &rim::Hub::getOffset,     &rim::HubWrap::defGetOffset)
       .def("_doTransaction", &rim::Hub::doTransaction, &rim::HubWrap::defDoTransaction)
   ;

   bp::implicitly_convertible<rim::HubPtr, rim::MasterPtr>();
   
}


//! Constructor
rim::HubWrap::HubWrap(uint64_t offset) : rim::Hub(offset) {}

//! Return offset
uint64_t rim::HubWrap::getOffset() {
   {
      rogue::ScopedGil gil;

      if (boost::python::override pb = this->get_override("_getOffset")) {
         try {
            return(pb());
         } catch (...) {
            PyErr_Print();
         }
      }
   }
   return(rim::Hub::getOffset());
}

//! Return offset
uint64_t rim::HubWrap::defGetOffset() {
   return(rim::Hub::getOffset());
}

//! Return offset
uint64_t rim::HubWrap::doAddress() {
   {
      rogue::ScopedGil gil;

      if (boost::python::override pb = this->get_override("_doAddress")) {
         try {
            return(pb());
         } catch (...) {
            PyErr_Print();
         }
      }
   }
   return(rim::Hub::doAddress());
}

//! Return offset
uint64_t rim::HubWrap::defDoAddress() {
   return(rim::Hub::doAddress());
}

//! Post a transaction. Master will call this method with the access attributes.
void rim::HubWrap::doTransaction(uint32_t id, rim::MasterPtr master,
                                   uint64_t address, uint32_t size, uint32_t type) {
   {
      rogue::ScopedGil gil;

      if (boost::python::override pb = this->get_override("_doTransaction")) {
         try {
            pb(id,master,address,size,type);
            return;
         } catch (...) {
            PyErr_Print();
         }
      }
   }
   rim::Hub::doTransaction(id,master,address,size,type);
}

//! Post a transaction. Master will call this method with the access attributes.
void rim::HubWrap::defDoTransaction(uint32_t id, rim::MasterPtr master,
                                      uint64_t address, uint32_t size, uint32_t type) {
   rim::Hub::doTransaction(id, master, address, size, type);
}

