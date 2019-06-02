package reference;

import reference.GMM.TextFileInput;

/**
 * Created by LinZheng on 2017/9/10.
 */
public class TestGMMUtil {
    public static void main(String[] args) {
        double[] weightings = new double[]{0.3625, 0.4005, 0.2371};
        double[] means = new double[]{4.2111, 5.4215, 5.8432};
        double[] sigmas = new double[]{0.234599766025, 0.303099797025, 3.575699466304};
        GMMUtil oGMM = new GMMUtil(Config.K,weightings,means,sigmas);
        String fileName = "src/reference/GMM/data.txt";
        int NumOfDataPoints = CountTotalDataPointsInFile(fileName);
        double[] datas = readFile(fileName, NumOfDataPoints);
        oGMM.print();
        oGMM.model(datas);
        oGMM.print();
    }

    public static double[] readFile(String fileName, int TotalDataPoints)        // Length of array to be filled
    {
        double[] alldatapoints = new double[TotalDataPoints];

        TextFileInput tfi = new TextFileInput(fileName);
        String line = tfi.readLine();
        int count = 0;
        while (line != null) {
//            alldatapoints[count] = Math.log(Double.parseDouble(line));
            alldatapoints[count] = Double.parseDouble(line);

            count++;
            line = tfi.readLine();
        }

        return alldatapoints;
    }

    public static int CountTotalDataPointsInFile(String fileName)        // length of array to be filled
    {
        int CountLine = 0;
        TextFileInput tfi = new TextFileInput(fileName);
        String line = tfi.readLine();
        while (line != null) {
            line = tfi.readLine();
            CountLine++;
        }

        return CountLine;
    }
}
