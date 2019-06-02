package thread.consume;

import IQ.IQnonlinear;
import IQ.IQnonlinearOld;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CyclicBarrier;

/**
 * Created by LinZheng on 2017/5/9.
 */
public class IQnonlinearConsumer extends IQConsumer {
    public IQnonlinearConsumer(BlockingQueue blockingQueue, CyclicBarrier cyclicBarrier) {
        super(blockingQueue, cyclicBarrier, new IQnonlinear());
    }
}
