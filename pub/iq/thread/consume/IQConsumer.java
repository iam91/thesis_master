package thread.consume;

//import old.IQ.IncrementalQuantile;
import IQ.IncrementalQuantile;
import reference.Config;

import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.Callable;
import java.util.concurrent.CyclicBarrier;

/**
 * Created by LinZheng on 2017/5/9.
 */
public class IQConsumer implements Callable<double[]> {

    protected BlockingQueue<List> blockingQueue;
    protected CyclicBarrier cyclicBarrier;
    protected IncrementalQuantile iq;

    public IQConsumer(BlockingQueue blockingQueue, CyclicBarrier cyclicBarrier, IncrementalQuantile iq) {
        this.blockingQueue = blockingQueue;
        this.cyclicBarrier = cyclicBarrier;
        this.iq = iq;
    }


    @Override
    public double[] call() throws Exception {
        while (true) {
            if (blockingQueue.size() > 0) {
                List<Double> dataList = blockingQueue.peek();
                if (dataList == null || dataList.size() == 0) break;
                iq.update(dataList);
                cyclicBarrier.await();
                if (dataList.size() < Config.N) break;
            }
        }
        return iq.getQuantile();
    }
}
