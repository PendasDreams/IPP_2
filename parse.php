<?php
    
    ini_set('display_error', 'stderr');

    function nothing($gen, $instruction, $order)
    {
        xmlwriter_start_element($gen, "instruction");
        xmlwriter_start_attribute($gen, "order");
        xmlwriter_text($gen, $order);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_attribute($gen, "opcode");
        xmlwriter_text($gen, $instruction);
        xmlwriter_end_attribute($gen);
        xmlwriter_end_element($gen);
    }

    function symbol($gen, $instruction, $order, $arg)
    {
        xmlwriter_start_element($gen, "instruction");
        xmlwriter_start_attribute($gen, "order");
        xmlwriter_text($gen, $order);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_attribute($gen, "opcode");
        xmlwriter_text($gen, $instruction);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_element($gen, "arg1");
        xmlwriter_start_attribute($gen, "type");
        if (preg_match("/^(GF@|LF@|TF@)/", $arg))
        {
            xmlwriter_text($gen, "var");
        }
        else if (preg_match("/^string@(?:[^\s\\#]|(\\[0-9]{3}))*$/u", $arg))
        {
            $arg= preg_replace("/^(string@)/", "", $arg);
            xmlwriter_text($gen, "string");    
            
        }
        else if (preg_match("/^int@[+-]?[0-9]+$/u", $arg))
        {
            $arg= preg_replace("/^(int@)/", "", $arg);
            xmlwriter_text($gen, "int");     
        }
        else if (preg_match("/^bool@(true|false)$/u", $arg))
        {
            $arg= preg_replace("/^(bool@)/", "", $arg);
            xmlwriter_text($gen, "bool");     
        }
        else if (preg_match("/^nil@nil$/u", $arg))
        {
            $arg= preg_replace("/^(nil@)/", "", $arg);
            xmlwriter_text($gen, "nil");     
        }
        else
        {
            fwrite(STDERR, "Variable Error\n");
            exit(23);
        }
        xmlwriter_end_attribute($gen);
        xmlwriter_text($gen, $arg);
        xmlwriter_end_element($gen);
        xmlwriter_end_element($gen);
    }
    function variable($gen, $instruction, $order, $arg)
    {
        xmlwriter_start_element($gen, "instruction");
        xmlwriter_start_attribute($gen, "order");
        xmlwriter_text($gen, $order);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_attribute($gen, "opcode");
        xmlwriter_text($gen, $instruction);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_element($gen, "arg1");
        xmlwriter_start_attribute($gen, "type");
        xmlwriter_text($gen, "var");
        xmlwriter_end_attribute($gen);
        if (preg_match("/^(GF@|LF@|TF@)/", $arg)== 0)
        {
            fwrite(STDERR, "Variable Error\n");
            exit(23);
        }
        xmlwriter_text($gen, $arg);
        xmlwriter_end_element($gen);
        xmlwriter_end_element($gen);
    }

    function type($gen, $instruction, $order, $arg1, $arg2)
    {
        xmlwriter_start_element($gen, "instruction");
        xmlwriter_start_attribute($gen, "order");
        xmlwriter_text($gen, $order);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_attribute($gen, "opcode");
        xmlwriter_text($gen, $instruction);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_element($gen, "arg1");
        xmlwriter_start_attribute($gen, "type");
        xmlwriter_text($gen, "var");
        xmlwriter_end_attribute($gen);
        if (preg_match("/^(GF@|LF@|TF@)/", $arg1)== 0)
        {
             fwrite(STDERR, "Problem with variable\n"); 
            exit(23);
        }
        xmlwriter_text($gen, $arg1);
        xmlwriter_end_element($gen);
        xmlwriter_start_element($gen, "arg2");
        xmlwriter_start_attribute($gen, "type");
        if (preg_match("/^(string|bool|int|nil)$/", $arg2))
        {
            xmlwriter_text($gen, "type");
        }
        else {
             fwrite(STDERR, "Variable Error\n");
            exit(23);
        }
        xmlwriter_end_attribute($gen);
        xmlwriter_text($gen, $arg2);
        xmlwriter_end_element($gen);
        xmlwriter_end_element($gen);
    }
    function variablesymbol($gen, $instruction, $order, $arg1, $arg2)
    {
        xmlwriter_start_element($gen, "instruction");
        xmlwriter_start_attribute($gen, "order");
        xmlwriter_text($gen, $order);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_attribute($gen, "opcode");
        xmlwriter_text($gen, $instruction);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_element($gen, "arg1");
        xmlwriter_start_attribute($gen, "type");
        xmlwriter_text($gen, "var");
        xmlwriter_end_attribute($gen);
        if (preg_match("/^(GF@|LF@|TF@)/", $arg1)== 0)
        {
             fwrite(STDERR, "Variable Error\n");
            exit(23);
        }
        xmlwriter_text($gen, $arg1);
        xmlwriter_end_element($gen);
        xmlwriter_start_element($gen, "arg2");
        xmlwriter_start_attribute($gen, "type");
        if (preg_match("/^(GF@|LF@|TF@)/", $arg2))
        {
            xmlwriter_text($gen, "var");
        }
        else if (preg_match("/^string@(?:[^\s\\#]|(\\[0-9]{3}))*$/u", $arg2))
        {
            $arg2= preg_replace("/^(string@)/", "", $arg2);
            xmlwriter_text($gen, "string");     
        }
        else if(preg_match("/^int@[+-]?[0-9]+$/u", $arg2))
        {
            $arg2= preg_replace("/^(int@)/", "", $arg2);
            xmlwriter_text($gen, "int");     
        }
        else if(preg_match("/^bool@(true|false)$/u", $arg2))
        {
            $arg2= preg_replace("/^(bool@)/", "", $arg2);
            xmlwriter_text($gen, "bool");     
        }
        else if (preg_match("/^nil@nil$/u", $arg2))
        {
            $arg2= preg_replace("/^(nil@)/", "", $arg2);
            xmlwriter_text($gen, "nil");     
        }
        else
        {
            fwrite(STDERR, "Variable Error\n"); 
            exit(23);
        }
        xmlwriter_end_attribute($gen);
        xmlwriter_text($gen, $arg2);
        xmlwriter_end_element($gen);
        xmlwriter_end_element($gen);
    }
    function variablesymbol2($gen, $instruction, $order, $arg1, $arg2, $arg3)
    {
        xmlwriter_start_element($gen, "instruction");
        xmlwriter_start_attribute($gen, "order");
        xmlwriter_text($gen, $order);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_attribute($gen, "opcode");
        xmlwriter_text($gen, $instruction);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_element($gen, "arg1");
        xmlwriter_start_attribute($gen, "type");
        xmlwriter_text($gen, "var");
        xmlwriter_end_attribute($gen);
        if (preg_match("/^(GF@|LF@|TF@)/", $arg1)== 0)
        {
            fwrite(STDERR, "Variable Error\n");
            exit(23);
        }
        xmlwriter_text($gen, $arg1);
        xmlwriter_end_element($gen);
        xmlwriter_start_element($gen, "arg2");
        xmlwriter_start_attribute($gen, "type");
        if (preg_match("/^(GF@|LF@|TF@)/", $arg2))
        {
            xmlwriter_text($gen, "var");
        }
        else if (preg_match("/^string@(?:[^\s\\#]|(\\[0-9]{3}))*$/u", $arg2))
        {
            $arg2= preg_replace("/^(string@)/", "", $arg2);
            xmlwriter_text($gen, "string");     
        }
        else if (preg_match("/^int@[+-]?[0-9]+$/u", $arg2))
        {
            $arg2= preg_replace("/^(int@)/", "", $arg2);
            xmlwriter_text($gen, "int");     
        }
        else if (preg_match("/^bool@(true|false)$/u", $arg2))
        {
            $arg2= preg_replace("/^(bool@)/", "", $arg2);
            xmlwriter_text($gen, "bool");     
        }
        else if (preg_match("/^nil@nil$/u", $arg2))
        {
            $arg2= preg_replace("/^(nil@)/", "", $arg2);
            xmlwriter_text($gen, "nil");     
        }
        else
        {
            fwrite(STDERR, "Variable Error\n"); 
            exit(23);
        }
        xmlwriter_end_attribute($gen);
        xmlwriter_text($gen, $arg2);
        xmlwriter_end_element($gen);
        xmlwriter_start_element($gen, "arg3");
        xmlwriter_start_attribute($gen, "type");
        if (preg_match("/^(GF@|LF@|TF@)/", $arg3))
        {
            xmlwriter_text($gen, "var");
        }
        else if(preg_match("/^string@(?:[^\s\\#]|(\\[0-9]{3}))*$/u", $arg3))
        {
            $arg3= preg_replace("/^(string@)/", "", $arg3);
            xmlwriter_text($gen, "string");     
        }
        else if (preg_match("/^int@[+-]?[0-9]+$/u", $arg3))
        {
            $arg3= preg_replace("/^(int@)/", "", $arg3);
            xmlwriter_text($gen, "int");     
        }
        else if (preg_match("/^bool@(true|false)$/u", $arg3))
        {
            $arg3= preg_replace("/^(bool@)/", "", $arg3);
            xmlwriter_text($gen, "bool");     
        }
        else if (preg_match("/^nil@nil$/u", $arg3))
        {
            $arg3= preg_replace("/^(nil@)/", "", $arg3);
            xmlwriter_text($gen, "nil");     
        }
        else
        {
            fwrite(STDERR, "Variable Error\n");
            exit(23);
        }
        xmlwriter_end_attribute($gen);
        xmlwriter_text($gen, $arg3);
        xmlwriter_end_element($gen);

        xmlwriter_end_element($gen);
    }
    function variablelabel($gen, $instruction, $order, $arg1, $arg2, $arg3)
    {
        xmlwriter_start_element($gen, "instruction");
        xmlwriter_start_attribute($gen, "order");
        xmlwriter_text($gen, $order);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_attribute($gen, "opcode");
        xmlwriter_text($gen, $instruction);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_element($gen, "arg1");
        xmlwriter_start_attribute($gen, "type");
        xmlwriter_text($gen, "label");
        xmlwriter_end_attribute($gen);
        xmlwriter_text($gen, $arg1);
        xmlwriter_end_element($gen);
        xmlwriter_start_element($gen, "arg2");
        xmlwriter_start_attribute($gen, "type");
        if (preg_match("/^(GF@|LF@|TF@)/", $arg2))
        {
            xmlwriter_text($gen, "var");
        }
        else if (preg_match("/^string@(?:[^\s\\#]|(\\[0-9]{3}))*$/u", $arg2))
        {
            $arg2= preg_replace("/^(string@)/", "", $arg2);
            xmlwriter_text($gen, "string");
        }
        else if (preg_match("/^int@[+-]?[0-9]+$/u", $arg2))
        {
            $arg2= preg_replace("/^(int@)/", "", $arg2);
            xmlwriter_text($gen, "int");
        }
        else if (preg_match("/^bool@(true|false)$/u", $arg2))
        {
            $arg2= preg_replace("/bool@/", "", $arg2);
            xmlwriter_text($gen, "bool");
        }
        else if (preg_match("/^nil@nil$/u", $arg2))
        {
            $arg2= preg_replace("/^(nil@)/", "", $arg2);
            xmlwriter_text($gen, "nil");
        }
        else
        {
            fwrite(STDERR, "Variable Error\n");
            exit(23);
        }
        xmlwriter_end_attribute($gen);
        xmlwriter_text($gen, $arg2);
        xmlwriter_end_element($gen);
        xmlwriter_start_element($gen, "arg3");
        xmlwriter_start_attribute($gen, "type");
        if (preg_match("/^(GF@|LF@|TF@)/", $arg3))
        {
            xmlwriter_text($gen, "var");
        }
        else if (preg_match("/^string@(?:[^\s\\#]|(\\[0-9]{3}))*$/u", $arg3))
        {
            $arg3= preg_replace("/^(string@)/", "", $arg3);
            xmlwriter_text($gen, "string");     
        }
        else if(preg_match("/^int@[+-]?[0-9]+$/u", $arg3))
        {
            $arg3= preg_replace("/^(int@)/", "", $arg3);
            xmlwriter_text($gen, "int");     
        }
        else if (preg_match("/^bool@(true|false)$/u", $arg3))
        {
            $arg3= preg_replace("/^(bool@)/", "", $arg3);
            xmlwriter_text($gen, "bool");     
        }
        else if (preg_match("/^nil@nil$/u", $arg3))
        {
            $arg3= preg_replace("/^(nil@)/", "", $arg3);
            xmlwriter_text($gen, "nil");     
        }
        else
        {
            fwrite(STDERR, "Variable Error\n"); 
            exit(23);
        }
        xmlwriter_end_attribute($gen);
        xmlwriter_text($gen, $arg3);
        xmlwriter_end_element($gen);
        xmlwriter_end_element($gen);
    }
    function label($gen, $instruction, $order, $arg)
    {
        xmlwriter_start_element($gen, "instruction");
        xmlwriter_start_attribute($gen, "order");
        xmlwriter_text($gen, $order);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_attribute($gen, "opcode");
        xmlwriter_text($gen, $instruction);
        xmlwriter_end_attribute($gen);
        xmlwriter_start_element($gen, "arg1");
        xmlwriter_start_attribute($gen, "type");
        xmlwriter_text($gen, "label");
        xmlwriter_end_attribute($gen);
        xmlwriter_text($gen, $arg);
        xmlwriter_end_element($gen);
        xmlwriter_end_element($gen);
    }

    function help($argc)
    {
        $auxilary= array("help");
        $auxilary2=getopt(NULL,$auxilary);
        if ($argc==2 && array_key_exists("help",$auxilary2))
        {
            echo "IPP Project 1 - parse.php help\n\n";
  			echo "This script takes input in IPPcode21 language and turns it into " .
  			"equivalent XML representation. Extension STATP is implemented too. " .
			"\n\n";
			echo "COMPATIBILITY:\nThis script was intended to run on PHP 7.4.\n\n";
			echo "USAGE:\nphp parse.php [ OPTIONS ] < input.src\n";
			echo "Script expects input on the standard command line input.\n\n";
			echo "OPTIONS:\n";
			echo "--stats=filename  This parameter enables statistics. Statistics will be " .
			"printed after the script finishes into the specified file (must be used with " .
			"one or more of: --loc, --comments, --labels, --jumps)\n";
			echo "--loc             This outputs number of lines with code into the statistic " .
			"(can't be used w/o --stats)\n";
			echo "--comments        Prints number of comments into the statistic (can't " .
			"be used w/o --stats)\n";
			echo "--jumps           Prints number of jump instructionuctions into the statistic " .
			"(can't be used w/o --stats)\n";
			echo "--labels          Prints number of defined labels into the statistic " .
			"(can't be used w/o --stats)\n";
            exit(0);
        }
        else if ($argc>1)
        {
            fwrite(STDERR, "wrong number of parameters or problem with parameters\n");
            exit(23);
        }
    }
    help($argc);
    
    $line= trim(fgets(STDIN));

    $pattern = ".IPPCODE21";

    for ($i = 0; $i < 10; $i++) 
    {
        if (strtoupper($line[$i]) != $pattern[$i])
        {
            if ($line[$i] == "#" || $line == "") 
            {
                $line= trim(fgets(STDIN));
                $i = 0;
            }
            else
            {
                fwrite(STDERR, "Starting atribute .IPPcode21 not found\n"); 
                exit(21);
            }
        }
    }

    $gen= xmlwriter_open_uri("php://stdout");
    xmlwriter_set_indent($gen, 1);
    xmlwriter_set_indent_string($gen, '  ');
    xmlwriter_start_document($gen, '1.0', 'utf-8');  
    xmlwriter_start_element($gen, "program");
    xmlwriter_start_attribute($gen, "language");
    xmlwriter_text($gen, "IPPcode21");
    xmlwriter_end_attribute($gen);
    $order= 1;
    while (($line= fgets(STDIN)))
    {  
        $line= trim($line);
        $divided= preg_split('/#/', $line);

        if ($divided[0]=="")
        { 
            continue;
        }
        else
        {
            $line=$divided[0]; 
        }
        $line= trim($line);

        $divided= preg_split('/\s+/', $line);
        if ($divided[0]=="")
        {
            continue;
        }
        $instruction= $divided[0];
        switch($instruction)
        {
            case 'MOVE':
                if (count($divided)==3)
                {
                	variablesymbol($gen,$instruction,$order,$divided[1],$divided[2]); 
                }  
                else {
                    exit(23);
                } 
                break;
            case 'STRLEN':
                if (count($divided)==3)
                {
                    variablesymbol($gen,$instruction,$order,$divided[1],$divided[2]); 
                }  
                else {
                    exit(23);
                } 
                break;
            case 'INT2CHAR':
                if (count($divided)==3)
                {
                    variablesymbol($gen,$instruction,$order,$divided[1],$divided[2]); 
                }  
                else {
                    exit(23);
                } 
                break;
            case 'TYPE':
                if (count($divided)==3)
                {
                    variablesymbol($gen,$instruction,$order,$divided[1],$divided[2]); 
                }  
                else {
                    exit(23);
                } 
                break;
            case 'NOT':
                if (count($divided)==3)
                {
                    variablesymbol($gen,$instruction,$order,$divided[1],$divided[2]);
                }
            	else {
                	exit(23);
            	} 
            	break;
            case 'PUSHFRAME':
                if (count($divided)==1)
                {
                    nothing($gen, $instruction, $order);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'CREATEFRAME':
                if (count($divided)==1)
                {
                    nothing($gen, $instruction, $order);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'POPFRAME':
                if (count($divided)==1)
                {
                    nothing($gen, $instruction, $order);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'BREAK':
                if (count($divided)==1)
                {
                    nothing($gen, $instruction, $order);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'RETURN':
                if (count($divided)==1)
                {
                    nothing($gen, $instruction, $order);
                }  
                else {
                    exit(23);
                } 
                break; 
            case 'ADD':
                if (count($divided)==4)
                {
                    variablesymbol2($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'MUL':
                if (count($divided)==4)
                {
                    variablesymbol2($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'SUB':
                if (count($divided)==4)
                {
                    variablesymbol2($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                } 
                break; 
            case 'IDIV':
                if (count($divided)==4)
                {
                    variablesymbol2($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'GT':
                if (count($divided)==4)
                {
                    variablesymbol2($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'LT':
                if (count($divided)==4)
                {
                    variablesymbol2($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'OR':
                if (count($divided)==4)
                {
                    variablesymbol2($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                }
                break;
            case 'EQ':
                if (count($divided)==4)
                {
                    variablesymbol2($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'AND':
                if (count($divided)==4)
                {
                    variablesymbol2($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'GETCHAR':
                if (count($divided)==4)
                {
                    variablesymbol2($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                } 
                break; 
            case 'CONCAT':
                if (count($divided)==4)
                {
                    variablesymbol2($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'STRI2INT':
                if (count($divided)==4)
                {
                    variablesymbol2($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'SETCHAR':
                if (count($divided)==4)
                {
                    variablesymbol2($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                } 
                break; 
            case 'POPS':
                if (count($divided)==2)
                {
                    variable($gen,$instruction,$order,$divided[1]);
                }  
                else {
                    exit(23);
                } 
                break;  
            case 'DEFVAR':
                if (count($divided)==2)
                {
                    variable($gen,$instruction,$order,$divided[1]);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'CALL':
                if (count($divided)==2){
                    label($gen,$instruction,$order,$divided[1]);
                }  
                else{
                    exit(23);
                } 
                break;
            case 'LABEL':
                if (count($divided)==2)
                {
                    label($gen,$instruction,$order,$divided[1]);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'JUMP':
                if (count($divided)==2){
                    label($gen,$instruction,$order,$divided[1]);
                }  
                else{
                    exit(23);
                } 
                break;
            case 'DPRINT':
                if (count($divided)==2)
                {
                    symbol($gen,$instruction,$order,$divided[1]);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'PUSHS':
                if (count($divided)==2)
                {
                    symbol($gen,$instruction,$order,$divided[1]);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'EXIT':
                if (count($divided)==2)
                {
                    symbol($gen,$instruction,$order,$divided[1]);
                }  
                else {
                    exit(23);
                } 
                break; 
            case 'WRITE':
                if (count($divided)==2)
                {
                    symbol($gen,$instruction,$order,$divided[1]);
                }  
                else {
                    exit(23);
                } 
                break;
            case 'READ':
                if (count($divided)==3)
                {
                    type($gen,$instruction,$order,$divided[1],$divided[2]); 
                }  
                else {
                    exit(23);
                } 
                break;
            case 'JUMPIFEQ':
                if (count($divided)==4)
                {
                    variablelabel($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                } 
                break; 
            case 'JUMPIFNEQ':
                if (count($divided)==4)
                {
                    variablelabel($gen,$instruction,$order,$divided[1],$divided[2],$divided[3]);
                }  
                else {
                    exit(23);
                } 
                break;   
        }
        $order++;
    }
    xmlwriter_end_element($gen);
    xmlwriter_end_document($gen);
    xmlwriter_output_memory($gen);
?>