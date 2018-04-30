// Inspired by
// https://pdfbox.apache.org/1.8/cookbook/workingwithattachments.html

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.io.IOException;
import java.io.File;
import java.util.GregorianCalendar;
import java.util.Map;
import java.util.HashMap;
import java.nio.file.Paths;
import java.nio.file.Files;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDDocumentNameDictionary;
import org.apache.pdfbox.pdmodel.PDEmbeddedFilesNameTreeNode;

import org.apache.pdfbox.pdmodel.common.filespecification.PDComplexFileSpecification;
import org.apache.pdfbox.pdmodel.common.filespecification.PDEmbeddedFile;

import org.apache.pdfbox.exceptions.COSVisitorException;

public class AttachFileToPdf
{
    public static void main(String[] args) throws IOException, COSVisitorException
    {
        AttachFileToPdf app = new AttachFileToPdf();
        if( args.length != 3 )
        {
            app.usage();
        }
        else
        {
            app.doIt( args[0], args[1], args[2] );
        }
    }
    private void usage()
    {
        System.err.println(
            "usage: " + this.getClass().getName()
            + " input.pdf attached_file output.pdf" );
    }

    public void
    doIt( String inputFilename, String attachedFilename, String outputFilename )
        throws IOException, COSVisitorException
    {
        PDDocument document = PDDocument.load( new File(inputFilename) );

        PDEmbeddedFilesNameTreeNode efTree = new PDEmbeddedFilesNameTreeNode();

        PDComplexFileSpecification fs = new PDComplexFileSpecification();
        fs.setFile( attachedFilename );
        byte[] attachedData = Files.readAllBytes( Paths.get( attachedFilename ) );
        InputStream is = new ByteArrayInputStream( attachedData );
        PDEmbeddedFile ef = new PDEmbeddedFile( document, is );
        ef.setSize( attachedData.length );
        ef.setCreationDate( new GregorianCalendar() );
        fs.setEmbeddedFile( ef );

        Map efMap = new HashMap();
        efMap.put( "Source", fs );
        efTree.setNames( efMap );
        PDDocumentNameDictionary names =
            new PDDocumentNameDictionary( document.getDocumentCatalog() );
        names.setEmbeddedFiles( efTree );
        document.getDocumentCatalog().setNames( names );
        document.save( outputFilename );
    }

}

