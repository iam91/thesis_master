package IQ;

import reference.Util;

import java.util.Arrays;
import java.util.List;

/**
 * Created by LinZheng on 2017/5/9.
 */
public class IQnonlinear extends IQnonlinearOld {
    private static int updateCount = 0;
    private static final int updateCountCycle = 50;


    private void updatePInverseP() {
//        System.out.println(Arrays.toString(bufferQuantile));
//        System.out.println(Arrays.toString(pInverseP));
        for (int i = 0; i < M; i++) {
            pInverseP[i] = (pInverseP[i] * totalCount + M * bufferQuantile[i]) / (totalCount + M);
        }
        updateCount = 0;
    }

    @Override
    public void update(List dataList) {
        fill(dataList);
        if (totalCount > 0) {
            CDFQ();
        }
        ECDF();
//        ACDF();
        computeBracketQ();
        refillQ();
        updateCount++;
        if (updateCount >= 50) {
            updatePInverseP();
        }
    }
}
