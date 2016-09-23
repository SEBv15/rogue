/**
 *-----------------------------------------------------------------------------
 * Title         : SLAC Register Protocol (SRP) Transaction V3
 * ----------------------------------------------------------------------------
 * File          : TransactionV3.cpp
 * Author        : Ryan Herbst <rherbst@slac.stanford.edu>
 * Created       : 09/17/2016
 * Last update   : 09/17/2016
 *-----------------------------------------------------------------------------
 * Description :
 *    Class to track a transaction
 *-----------------------------------------------------------------------------
 * This file is part of the rogue software platform. It is subject to 
 * the license terms in the LICENSE.txt file found in the top-level directory 
 * of this distribution and at: 
    * https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html. 
 * No part of the rogue software platform, including this file, may be 
 * copied, modified, propagated, or distributed except according to the terms 
 * contained in the LICENSE.txt file.
 *-----------------------------------------------------------------------------
**/
#include <rogue/protocols/srp/TransactionV3.h>
#include <rogue/interfaces/stream/Frame.h>
#include <rogue/interfaces/memory/Block.h>
#include <boost/python.hpp>
#include <boost/thread.hpp>
#include <boost/make_shared.hpp>
#include <stdint.h>

namespace bp = boost::python;
namespace rps = rogue::protocols::srp;
namespace ris = rogue::interfaces::stream;
namespace rim = rogue::interfaces::memory;

//! Virtual init function
void rps::TransactionV3::init() {

   rxSize_ = (block_->getSize() + 24); // 5 x 32 bits for header, + 32-bit tail

   txSize_ = 20; // 5 x 32 bits for header
   if (write_) txSize_ += block_->getSize();

   // Header word 0
   header_[0] = 0x3;

   // Bits 9:8: 0x0 = read, 0x1 = write, 0x3 = posted write
   if ( write_ ) {
      if ( block_->getPostedWrite() ) header_[0] |= 0x20;
      else header_[0] |= 0x10;
   }
   
   // Bits 13:10 not used in gen frame
   // Bit 14 = ignore mem resp
   // Bit 14 = ignore mem resp
   // Bit 23:15 = Unused
   // Bit 31:24 = timeout count
 
   // Header word 1, transaction ID
   header_[1] = index_;

   // Header word 2, lower address
   header_[2] = block_->getAddress() & 0xFFFFFFFF;

   // Header word 3, upper address
   header_[3] = (block_->getAddress() >> 32) & 0xFFFFFFFF;

   // Header word 4, request size
   header_[4] = block_->getSize();
}

//! Generate request frame
bool rps::TransactionV3::intGenFrame(ris::FramePtr frame) {
   uint32_t cnt;
   uint32_t x;

   if ( (txSize_ == 0) || (frame->getAvailable() != txSize_) ) {
      block_->setError(1);
      return(false);
   }

   // header
   cnt = 0;
   for (x=0; x < 5; x++) cnt += frame->write(&(header_[x]),cnt,4);

   // Write data
   if ( write_ ) {
      for (x=0; x < block_->getSize()/4; x++) {
         cnt += frame->write(block_->getData()+(x*4),cnt,4);
      }
   }
   return(true);
}

//! Receive response frame
bool rps::TransactionV3::intRecvFrame(ris::FramePtr frame) {
   uint32_t rxHeader[5];
   uint32_t cnt;
   uint32_t tail;
   uint32_t x;

   if ( frame->getPayload() < rxSize_ ) return(false);

   // Extract header
   cnt = 0;
   for (x=0; x < 5; x++) cnt += frame->read(&(rxHeader[x]),cnt,4);

   // Compare headers
   if ( ((rxHeader[0] ^ header_[0]) & 0xFF00003F) != 0 ) return(false);
   if (  (rxHeader[1] ^ header_[1]) != 0 ) return(false);
   if (  (rxHeader[2] ^ header_[2]) != 0 ) return(false);
   if (  (rxHeader[3] ^ header_[3]) != 0 ) return(false);
   if (  (rxHeader[4] ^ header_[4]) != 0 ) return(false);
  
   // Read tail
   frame->read(&tail,frame->getPayload()-4,4);

   // Tail shows error
   if ( tail != 0 ) {
      block_->setError(tail);
      return(false);
   }

   // Copy payload if read
   if ( ! write_ ) {
      for (x=0; x < block_->getSize()/4; x++) {
         cnt += frame->read(block_->getData()+(x*4),cnt,4);
      }
   }

   block_->setStale(false);
   return(true); 
}

//! Class creation
rps::TransactionV3Ptr rps::TransactionV3::create (bool write, rim::BlockPtr block) {
   rps::TransactionV3Ptr t = boost::make_shared<rps::TransactionV3>(write,block);
   return(t);
}

//! Setup class in python
void rps::TransactionV3::setup_python() {
   // Nothing to do
}

//! Get transaction id
uint32_t rps::TransactionV3::extractTid (ris::FramePtr frame) {
   uint32_t tid;

   if ( frame->getPayload() < 20 ) return(0);

   frame->read(&tid,4,4);
   return(tid);
}

//! Creator with version constant
rps::TransactionV3::TransactionV3(bool write, rim::BlockPtr block) : Transaction(write,block) {
   // Nothing to do
}

//! Deconstructor
rps::TransactionV3::~TransactionV3() { 
   // Nothing to do
}
