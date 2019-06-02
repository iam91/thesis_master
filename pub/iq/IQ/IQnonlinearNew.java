package IQ;

import reference.Util;

import java.util.Arrays;
import java.util.List;

/**
 * Created by LinZheng on 2017/5/9.
 */
public class IQnonlinearNew extends IQnonlinearOld {
    private static int updateCount = 0;
    private static double mean = 5.178363;
    private static double sigma = 1.199186;


    protected static double pInverse(double y) {
//        if (y >= maxEnd) {
//            maxEnd = y + 1;
//        }
        if (y < 10E-4) {
            return 0.0;
        }
        double start = 0;
        double end = oGMM.maxEnd;      //1-p(end)<10E-6即可，大概为13.1最小，但误差偏大
        double mid = (start + end) / 2;
        double midY = p(mid);
        while (Math.abs(midY - y) > 10E-6) {
            if (midY > y) {
                end = mid;
            } else {
                start = mid;
            }
            mid = (start + end) / 2;
            midY = p(mid);
        }
        return mid;
    }

    protected static double p(double x) {
        double y = Util.normalDistribution(mean, sigma, x);
        return y;
    }

    private void updatePInverseP() {
//        mean = sum / (totalCount + N);
//        sigma = Math.sqrt((sum_2 - Math.pow(sum, 2) / (totalCount + N)) / (totalCount + N));
//        System.out.println(mean + " " + sigma);
//        System.out.println(Arrays.toString(bufferQuantile));
//        for (int i = 0; i < M; i++) {
//            pInverseP[i] = pInverse(probability[i]);
//        }
//        updateCount = 0;
    }

    @Override
    public void update(List dataList) {
        fill(dataList);
        if (totalCount > 0) {
            CDFQ();
        }
        ECDF();
        computeBracketQ();
        refillQ();
        updateCount++;
        if (updateCount >= 50) {
            updatePInverseP();
        }
    }
}
