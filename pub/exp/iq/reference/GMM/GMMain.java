package reference.GMM;

/**
 * Created by LinZheng on 2017/6/13.
 */
public class GMMain {
    public static GMModel Gmm;
    public static void main(String[] args) {             // main function

        Gmm = new GMModel();

        for(int i=0; i< Gmm.Threshold.length; i++){
            Gmm.GaussianMixtureModel(i);             // To build GM Model
            Gmm.OutputFinalReport(i);                // To Output Final Report
            Gmm.ResetValues();                       // Resetting Value for Next Threshold GMM
        }


    }  // Main function ends here..

}