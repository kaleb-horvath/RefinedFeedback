/**
 * Marks up supplied output according to how it matched a supplied regular expression (regex).
 * <p>The following regular expression elements are supported:
 * <ul>
 *   <li>Literals separated by the any character wildcard (".") and the zero or more modifer ("*")</li>
 * </ul>
 * @author Hyrum D. Carroll
 * @version 0.3 (Jan 21, 2022)
 */

import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Arrays;

public class RefinedRegexFeedback{

    private final static String USAGE = "Usage <regex> (with stdin containing the output to match up with the regex)";
    public final static String FLANKING_STR = "***";  // string appearing before and after matching literal

    public final static String PARAGRAPH_SYMBOL = "\u00B6"; // ¶, pilcrow (paragraph) symbol

    public static void DEBUG( String msg ){
        System.err.println("DEBUGGING: " + msg);            
    }

    public static void DEBUG( String[] a ){
        System.err.println("DEBUGGING: array (count: " + a.length + ")");
        for( String msg : a ){
            System.err.println("DEBUGGING:\t" + msg);
        }
    }


    /**
     * String.repeat() substitution
     * @param str the string to repeat count times
     * @param count number of times to repeat str
     * @return returns str repeated count times
     */
    public static String stringRepeat( String str, int count){
        StringBuilder repeatedStr = new StringBuilder();
        for( int i = 0; i < count; ++i){
            repeatedStr.append( str );
        }
        return repeatedStr.toString();
    }
    
    /**
     * Get all of the input from stdin
     * @return a string with all of the input from stdin
     */
    public static String getAllInput( ){
        StringBuilder input = new StringBuilder();
        try{
            BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));
            String line = "";
            while( (line = stdin.readLine()) != null ){
                input.append( line + "\n" );
            }
            stdin.close();
        }catch( IOException e){
            e.printStackTrace();
            System.exit(1);
        }
        return input.toString();
    }

    /**
     * Display the stacked view
     * @param expandedRegex regex string expanded to match character for character with outputStr
     * @param outputStr students output
     */
    private static void displayStackedView( String expandedRegex, String outputStr ){
        // display header
        System.out.println("Stacked Matches View");
        System.out.println("=================================");

        if( expandedRegex.length() == 0 || outputStr.length() == 0){
            System.out.println("(no matches)\n\n");
            return;
        }
        
        // For each line, display the students output and the expanded regular expression
        String[] outputLines = outputStr.split( PARAGRAPH_SYMBOL );
        int previousLineI = -1; // index of the last character in the previous line of outputStr
        int outputLinesI = 0; // index of outputLines

        // while there's output lines and expanded regex to display
        while( outputLinesI < outputLines.length && previousLineI < expandedRegex.length() ){
            String line = outputLines[outputLinesI]; // does not include the paragragph marker / newline
            // System.out.print( line.substring(0, Math.min( line.length(), expandedRegex.length() - previousLineI - 1)));
            if( expandedRegex.length() - previousLineI - 1 <= line.length() ){
                // don't display all of the expandedRegex
                System.out.println( line.substring(0, expandedRegex.length() - previousLineI - 1) + " (student output)");
            }else{
                System.out.println( line + PARAGRAPH_SYMBOL + " (student output)");
            }
            System.out.println( expandedRegex.substring( previousLineI + 1, Math.min(previousLineI + 1 + line.length() + 1, expandedRegex.length()) ) + " (expanded regular expression)");
            previousLineI += line.length() + 1;
            System.out.println();
            ++outputLinesI;
        }
        System.out.println();
    }

    
    /**
     * Display the annotated view
     * @param capitalizedOutput marked up students output
     */
    private static void displayAnnotatedViewed( String capitalizedOutput ){
        System.out.println("Annotated Matches View");
        System.out.println("=================================");
        if( capitalizedOutput.length() == 0){
            System.out.println("(no matches)\n");
        }else{
            System.out.println( capitalizedOutput.replace( PARAGRAPH_SYMBOL, PARAGRAPH_SYMBOL + "\n") + "\n" );
        }
    }

    
    public static void main( String[] args ){
        /* Get the regular expression from the command-line */

        if( args.length < 1 ){
            System.err.println("ERROR: Only found " + args.length + " command-line arguments.\n");
            System.err.println(USAGE + "\n");
            System.exit(1);
        }

        // regex
        String regex = args[0];
        DEBUG("regex: " + regex);

        String outputStr = getAllInput();
        DEBUG( "outputStr (" + outputStr.length() + " characters): " + outputStr);
        outputStr = outputStr.replace("\n", PARAGRAPH_SYMBOL ); // replace all newlines with the 
        
 // Future:
        // for each regular expression element, match against submission:
        //     .*/.+: while the submission does not match the first character of the next regex element
        //     Character class: Check for a match for each character
        //     Group: Check for a match for option

        //
        // Build strings for the expanded regex (BLAST-like) string and the annotated output (with flanking "***"s and capitalized matches)
        // 
        // Get array of literals in regex by splitting it by .*
        // For each literal, find the match in the output, starting from the index of the previous match
        // + Expanded regex: include "." for each character since the last match, then include the literal
        // + Annotated output: 

        // for each token in the regex
        String[] literals = regex.split("\\.\\*");
        DEBUG( literals );

        int literalsI = 0;
        int matchI = -1;  // the index in outputStr that matches the current literal
        int lastMatchI = -1; // index in outputStr of the last match (last character of the last matched literal)

        StringBuilder expandedRegex = new StringBuilder(); // For top (regex) and bottom (output) (BLAST-like)
        StringBuilder capitalizedOutput = new StringBuilder(); // For matched literals captialized and flanked with ***

        // go through each literal that is found in the output string
        while( literalsI < literals.length && (matchI = outputStr.indexOf( literals[literalsI], lastMatchI + 1)) >= 0 ){
            String literal = literals[literalsI];
            DEBUG("literal: " + literal);
            DEBUG("literalsI: " + literalsI);
            DEBUG("matchI: " + matchI);

            String regexFiller = ".";
            if( literalsI == 0 ){
                // for the first occurence, use space instead
                regexFiller = " ";
            }
            expandedRegex.append( stringRepeat( regexFiller, matchI - (lastMatchI + 1) ) );  // ..... for in between literals
            expandedRegex.append( literal );                    // matching literal
            DEBUG("expandedRegex: " + expandedRegex);
            
            capitalizedOutput.append( outputStr.substring( lastMatchI + 1, matchI ) ); // copy of output for in between literals
            capitalizedOutput.append( FLANKING_STR + literal.toUpperCase() + FLANKING_STR ); // capitalized literal with flanking strings
            DEBUG("capitalizedOutput: " + capitalizedOutput);

            lastMatchI = matchI + literal.length() - 1;   // reposition the last matched index
            DEBUG("lastMatchI: " + lastMatchI);
            DEBUG("");
            ++literalsI;
        }
        if( literalsI == literals.length ){
            expandedRegex.append( stringRepeat( " ", outputStr.length() - (lastMatchI + 1) ) );
            capitalizedOutput.append( outputStr.substring( lastMatchI + 1, outputStr.length() ) ); // copy of output until the end
        }
        
        // add in newlines to stacked output string (as many are applicable) (based on the location of the newlines in the output string
        System.out.println();

        // if not all of the literals were found, then display the remaining ones
        System.out.println();
        if( literalsI == 0 ){
            String unmatchedRegex = String.join(".*", Arrays.copyOfRange( literals, literalsI, literals.length));
            System.out.println("Unable to find any matches for the regular expression: \"" + unmatchedRegex + "\".");
            System.out.println("Your output was:\n");
            System.out.println( outputStr.replace( PARAGRAPH_SYMBOL, PARAGRAPH_SYMBOL + "\n") );
        }else{
            displayStackedView( expandedRegex.toString(), outputStr.toString() );
            displayAnnotatedViewed( capitalizedOutput.toString() );

            if( literalsI != literals.length ){
                String unmatchedRegex = String.join(".*", Arrays.copyOfRange( literals, literalsI, literals.length));
                System.out.println("Unable to find a match for the rest of the regular expression: \"" + unmatchedRegex + "\".");
                System.out.println("The unmatch portion of the output is:\n");
                System.out.println( outputStr.substring( lastMatchI + 1 ).replace( PARAGRAPH_SYMBOL, PARAGRAPH_SYMBOL + "\n") );
            }else{
                System.out.println("All regular expressions terms found!  Good job!");
            }
        }
    }
}
