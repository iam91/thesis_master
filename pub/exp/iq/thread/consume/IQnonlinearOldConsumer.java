package thread.consume;

import IQ.IQnonlinearOld;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CyclicBarrier;

/**
 * Created by LinZheng on 2017/5/9.
 */
public class IQnonlinearOldConsumer extends IQConsumer {
    public IQnonlinearOldConsumer(BlockingQueue blockingQueue, CyclicBarrier cyclicBarrier) {
        super(blockingQueue, cyclicBarrier, new IQnonlinearOld());
    }
}
