import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.SparkFiles

// $example on$
import org.apache.spark.mllib.feature.{HashingTF, Normalizer}
import org.apache.spark.mllib.linalg.Vector
import org.apache.spark.mllib.linalg.distributed.{IndexedRowMatrix, IndexedRow}
import org.apache.spark.rdd.RDD
// $example off$

object TextSimilarity {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("TextSimilarity")
    val sc = new SparkContext(conf)

    //read documents
    //sc.addFile("input.txt")
    val documents: RDD[Seq[String]] = sc.textFile("/spark-data/input.txt").map(_.split(" ").toSeq)
    //val rawDocs: RDD[Seq[String]] = SparkFiles.get("input.txt").split("\n")  map(_.split(" ").toSeq)
    //println(SparkFiles.get("input.txt"))
    //val documents: RDD[Seq[String]] = sc.parallelize(SparkFiles.get("input.txt").split("\n")).map(_.split(" ").toSeq)
    //println(SparkFiles.get("input.txt").split("\n"))
    
    //apply Term Frequency to count terms in each documents
    val hashingTF = new HashingTF()
    val tf: RDD[Vector] = hashingTF.transform(documents)

    //normalize TF vectors
    val normalizer = new Normalizer()
    val indexed = normalizer.transform(tf).zipWithIndex()
    val normalized = indexed.map( v => new IndexedRow(v._2, v._1))

    
    val mat = new IndexedRowMatrix(normalized).toBlockMatrix()
    val dot = mat.multiply(mat.transpose)

    val local = dot.toLocalMatrix()
    val length = local.numRows
    val result = local.toArray
    //println(result.getClass.toString())
    for ( i <- 0 to length-1) printf("%3.2f\n", result(i)*100)
    //for (res <- result) println(res)

    sc.stop()
  }
}