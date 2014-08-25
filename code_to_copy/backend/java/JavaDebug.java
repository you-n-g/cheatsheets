public class JavaDebug {
    public static void main(String[] args) {
        // 输出debug信息
        for (StackTraceElement ste : Thread.currentThread().getStackTrace()) {
           System.out.println(ste);
        }

        // 睡一睡
        try {
            Thread.sleep(10000);
        } catch (InterruptedException ex) {
            Thread.currentThread().interrupt();
        }
    }
}
