package thread.consume;

import IQ.IQnonlinearNew;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CyclicBarrier;

/**
 * Created by LinZheng on 2017/5/9.
 */
public class IQnonlinearNewConsumer extends IQConsumer {
    public IQnonlinearNewConsumer(BlockingQueue blockingQueue, CyclicBarrier cyclicBarrier) {
        super(blockingQueue, cyclicBarrier, new IQnonlinearNew());
    }
}
