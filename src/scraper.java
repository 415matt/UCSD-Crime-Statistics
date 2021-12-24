import java.io.*;
import java.net.*;
import java.time.LocalDate;


/**
 * Scrapes all crime log pdf's from UCPD's website:
 * https://www.police.ucsd.edu/docs/reports/CallsandArrests/Calls_and_Arrests.asp
 */
public class Scraper {

    static final String[] MONTHS = {"January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"};

    /**
     * Returns the theoretical url for a given Calendar date
     * @param date - given date
     * @return - url as string
     */
    public String getURl(LocalDate date) {

        int m = date.getMonthValue() - 1;
        int day = date.getDayOfMonth();
        int year = date.getYear();

        String url = "https://www.police.ucsd.edu/docs/reports/CallsandArrests/CallsForService/"
                    + MONTHS[m] + "%20" + day + ",%20" + year + ".pdf";

        return url;
    }

    /**
     * Downloads the pdf at the specified URL
     * @param date - date of pdf to download
     * @return - True if successful, false otherwise.
     */
    public Boolean download(LocalDate date) {
        File filePath = new File("logs/" + date.toString() + ".pdf");

        //Don't bother, file already exists
        if (filePath.exists()) {
            return true;
        }

        // https://stackoverflow.com/a/20265955
        try {
            URL url = new URL(this.getURl(date));
            InputStream in = url.openStream();

            FileOutputStream fos = new FileOutputStream(filePath);

            int length = -1;
            byte[] buffer = new byte[1024]; // buffer for portion of data from connection
            while ((length = in.read(buffer)) > -1) {
                fos.write(buffer, 0, length);
            }

            fos.close();
            in.close();
        }

        //exception thrown
        catch (Exception e) {
            return true;
        }

        return true;
    }

    public static void main(String[] args) {
        String startDate = "2021-10-21";
        Scraper scraper = new Scraper();

        LocalDate currDate = LocalDate.parse(startDate);


        //downloads every pdf since specified startDate.
        //sometimes UCPD skips publishing days, so we terminate the loop only after 5 consecutive download fails
        int skips = 0;

        while (true) {

            //break condition
            if (skips > 4) {
                break;
            }

            //failed
            if (!scraper.download(currDate)) {
                skips++;
            }

            //successful
            else {
                skips = 0;
            }

            //increment date
            currDate = currDate.plusDays(1);

        }

    }


}
