#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import sys
import re
import argparse

class Parser():
    "Hack assembler language parser program."
    def __init__(self, asm):
        self.symTbl = self._init_symbles()
        self.src = asm
        self._var_addr = 16

    def _init_symbles(self):
        "populate the symble table with hack lang native symbles"
        sym_table = {
            'SP'   : 0,
            'LCL'  : 1,
            'ARG'  : 2,
            'THIS' : 3,
            'THAT' : 4,
            'R0' : 0,
            'R1' : 1,
            'R2' : 2,
            'R3' : 3,
            'R4' : 4,
            'R5' : 5,
            'R6' : 6,
            'R7' : 7,
            'R8' : 8,
            'R9' : 9,
            'R10' : 10,
            'R11' : 11,
            'R12' : 12,
            'R13' : 13,
            'R14' : 14,
            'R15' : 15,
            'SCREEN' : 16384,
            'KBD' : 24576,
            'DEST_M'  : '001',
            'DEST_D'  : '010',
            'DEST_MD' : '011',
            'DEST_A'  : '100',
            'DEST_AM' : '101',
            'DEST_AD' : '110',
            'DEST_AMD': '111',
            'JMP_JGT' : '001',
            'JMP_JEQ' : '010',
            'JMP_JGE' : '011',
            'JMP_JLT' : '100',
            'JMP_JNE' : '101',
            'JMP_JLE' : '110',
            'JMP_JMP' : '111',
            'CMP_0'   :'0101010',
            'CMP_1'   :'0111111',
            'CMP_-1'  :'0111010',
            'CMP_D'   :'0001100',
            'CMP_A'   :'0110000',
            'CMP_!D'  :'0001101',
            'CMP_!A'  :'0110001',
            'CMP_-D'  :'0001111',
            'CMP_-A'  :'0110011',
            'CMP_D+1' :'0011111',
            'CMP_A+1' :'0110111',
            'CMP_D-1' :'0001110',
            'CMP_A-1' :'0110010',
            'CMP_D+A' :'0000010',
            'CMP_D-A' :'0010011',
            'CMP_A-D' :'0000111',
            'CMP_D&A' :'0000000',
            'CMP_D|A' :'0010101',
            'CMP_M'   :'1110000',
            'CMP_!M'  :'1110001',
            'CMP_-M'  :'1110011',
            'CMP_M+1' :'1110111',
            'CMP_M-1' :'1110010',
            'CMP_D+M' :'1000010',
            'CMP_D-M' :'1010011',
            'CMP_M-D' :'1000111',
            'CMP_D&M' :'1000000',
            'CMP_D|M' :'1010101'           
        }
        return sym_table

    def _preparse(self):
        "strip all empty lines together with comments, resolve lables, variables"
        lines = []
        index = 0
        fullsrc = os.path.join(os.getcwd(), self.src)
        if os.path.exists(fullsrc):
            with open(fullsrc, 'r') as f:
                for line in f:
                    retline = self._strip(line)
                    if (retline):
                        retline = self._extract_lables(retline, index)
                        if (retline):
                            lines.append(retline)
                            index += 1

        else:
            print("ERR: source file not readable")
            return None
        return lines


    def _extract_lables(self, line, index):
        "helper function to extract labels, need to revisit"
        m = re.match(r'\((.+)\)', line)
        if m:
            label = m.group(1)
            self.symTbl[label] = index
            return None
        
        m = re.match(r'@([A-Za-z._]+\w+)$', line)
        if m:
            label = m.group(1)
            if label not in self.symTbl:
                self.symTbl[label] = self._var_addr
                self._var_addr += 1
                return line
        return line

            
    def _strip(self, line):
        "helper function of stripping comments, empty spaces"
        aline = line.strip().replace(' ', '')
        if not aline or re.match(r'^\s*$', aline) or re.match(r'\s*//.*', aline):
            return None
        elif re.match(r'.*//.*', aline):
            aline = re.sub(r'(.*)//.*', r'\1', aline)
            return aline.rstrip()
        else:
            return aline

    def _code(self, lines):
        "convert instructions(A, D) into binary format"
        codes = []
        for line in lines:
            bstr = None
            if line[0] == '@':
                bstr = self._convert_a_instruction(line)
            else:
                bstr = self._convert_c_instruction(line)
            if bstr:
                codes.append(bstr)
        return codes

    def _convert_a_instruction(self, line):
        " A Instruction convertor "
        label = line[1:]
        value = None
        if re.match('\d+', label):
            value = int(label)
        else:
            value = self.symTbl[label]
            
        bval = str(bin(value))[2:]
        rsize = len(bval)
        binIns = (16-rsize)*'0' + bval
        return binIns

    def _convert_c_instruction(self, line):
        " C Instruction convertor "
        prefix = "111"
        defjmp = "000"
        defdst = "000"
        binIns = None
        if ';' in line and '=' in line:
            parts = re.split(';=', line)
            binIns = prefix + self.symTbl['CMP_'+parts[1]] + self.symTbl['DEST_'+parts[1]] + self.symTbl['JMP_'+parts[2]]
        elif ';' in line:
            parts = re.split(';', line)
            binIns = prefix + self.symTbl['CMP_'+parts[0]] + defdst + self.symTbl['JMP_'+parts[1]]
        elif '=' in line:
            parts = re.split('=', line)
            binIns = prefix + self.symTbl['CMP_'+parts[1]] + self.symTbl['DEST_'+parts[0]] + defjmp
        return binIns
        

    def parse(self):
        "main parsing driver logic"
        lines = self._preparse()
        if (lines):
            lines = self._code(lines)
            if (lines):
                fulldst = os.path.join(os.getcwd(), self.src.replace('asm', 'hack'))
                with open(fulldst, 'w') as f:
                    for code in lines:
                        f.write('%s\n' % code)
        print("Done")


if __name__ == '__main__':
    argpar = argparse.ArgumentParser(description='Hack assembler args.')
    argpar.add_argument('asm', nargs=1, help='source assembly file')
    argpar.add_argument('-o', '--output', nargs=1, help='hack file')
    args = argpar.parse_args()
    
    parser = Parser(args.asm[0])
    parser.parse()
