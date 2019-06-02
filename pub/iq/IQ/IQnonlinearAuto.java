package IQ;

import reference.Config;

import java.util.List;

/**
 * Created by LinZheng on 2017/9/10.
 */
public class IQnonlinearAuto extends IQnonlinearOld {
    private static int updateCount = 0;

    private void updatePInverseP() {

        oGMM.model(bufferQuantile);

//        oGMM.print();
        oGMM.initStartEnd();
        for (int i = 0; i < M; i++) {
            pInverseP[i] = oGMM.pInverse(probability[i]);
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
        computeBracketQ();
        refillQ();
        updateCount++;
        if (updateCount > 0) {
            updatePInverseP();
        }
    }

}
