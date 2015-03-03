public class JavaDebug {

    // 遍历文件夹,  java8 有更好的实现
    public void listFilesForFolder(final File folder) {
        for (final File fileEntry : folder.listFiles()) {
            if (fileEntry.isDirectory()) {
                listFilesForFolder(fileEntry);
            } else {
                System.out.println(fileEntry.getName());
            }
        }
    }

    final File folder = new File("/home/you/XXX_PATH");
    listFilesForFolder(folder);


    // 读取文件
    // 函数外层要加 throws IOException
    BufferedReader br = new BufferedReader(new FileReader("XXXX.txt"));
    String line;
    try {
        StringBuilder sb = new StringBuilder();
        line = br.readLine();

        while (line != null) {
            sb.append(line);
            sb.append(System.lineSeparator());
            line = br.readLine();
        }
        String everything = sb.toString();
    } finally {
        br.close();
    }

    // 写文件 (个方法会直接覆盖文件???)
    //Writer writer = null;
    BufferedWriter writer = null;
    try {
        writer = new BufferedWriter(new OutputStreamWriter(
              new FileOutputStream("XXXXX.txt"), "utf-8"));
        writer.write("Something");
        writer.newLine();
    } catch (IOException ex) {
      // report
    } finally {
       try {writer.close();} catch (Exception ex) {}
    }


    // LOG
    // TODO 用哪个Logger????
    private static final Logger log = Logger.getLogger( CorpusIndexMaker.class.getName() );
    log.info("Begin Loading listFilesForFolder....");


    public static void main(String[] args) {
    }



    // 坑！！！！！！！
    // ArrayList 转 Array居然要这样， 而不是直接 toArray
    List<String> list = ..;
    String[] array = list.toArray(new String[list.size()]);
}
