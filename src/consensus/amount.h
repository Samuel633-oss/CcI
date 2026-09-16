// Copyright (c) 2009-2010 Satoshi Nakamoto
// Copyright (c) 2009-present The Alara Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef ALARA_CONSENSUS_AMOUNT_H
#define ALARA_CONSENSUS_AMOUNT_H

#include <cstdint>

/** Amount in satoshis (Can be negative) */
typedef int64_t CAmount;

/** The amount of satoshis in one ALA. */
inline constexpr CAmount COIN{100'000'000};

/** No amount larger than this (in satoshi) is valid.
 *
 * Note that this constant IS the total money supply for Alara.
 * 21,000,000 ALA fixed supply. This is consensus critical.
 * */
inline constexpr CAmount MAX_MONEY{21'000'000 * COIN};
inline bool MoneyRange(const CAmount& nValue) { return (nValue >= 0 && nValue <= MAX_MONEY); }

#endif // ALARA_CONSENSUS_AMOUNT_H
