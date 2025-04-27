# Panel-Method 面元法
这是由本人所编写的二维面元法(Panel Method)程序,可以求解一个空间中多个机翼情况的势流问题。这个面元法的算法参见PanelMethod-VT.pdf。

以下介绍其中(文件夹panel method中)各程序之功用:
    
    1. aifoil.py,landscape.py,geometry.py:定义了自定义对象airfoil(机翼),landscape(可以认为是多个机翼藕合而成的图),points,edges等,并且把几何计算的步骤放在了geomertry.py之中。
    2. data_process,data_process_N:数据处理工作,包含了从读入翼型数据(已经是read.py使用过后的输出)到存储计算结果的全过程。.._N.py是对于多个机翼的版本。
    3. geo_compute.py和geometry.py同功用,但是老版本。
    4. matrix_composition.py:包含了对矩阵A的拼接过程。
    5. read.py:处理读入翼型坐标到存储翼型数据的过程,注意这一步没有被data_process中涵盖。
    6. solver.py,solverN.py:是求解方法也。
    7. write.py:可以从已经存储好的数据中读出并且写在某个文件中,用于比对数据。
    8. data_generate.py:若需要训练神经网络,或许可以通过类似于此的程序生成数据。

此外,我在Josh The Engineer先生的代码(参见[JTE0419PanelMethod](https://github.com/jte0419/Panel_Methods))中发现了一点问题,记录在了文件(Josh代码中的错误.txt中).希望可以与Josh先生核证以促进共同进步。

限于本人英语水平,以上皆以汉语表达,若有外国友人不能阅读,深表抱歉。