<template>
    <div>
        <div class="container">

            <el-container>
                <el-header>神经网络框架图</el-header>
                <div class="demo-image__preview">
                    <el-image
                        :src="tnnurl"
                        :preview-src-list="srcList"
                        :fit="fit"
                    >

                    </el-image>
                </div>
            </el-container>

            <el-divider></el-divider>

            <el-container>
                <el-row>
                    <span>设计思想介绍:</span>
                    <i class="el-icon-s-opportunity" style="padding-left: 2px"></i>
                </el-row>

                <br>
                <div class="introduction">
                    <div>&emsp;&emsp;LSTM是RNN的一个变种，RNN的每一次隐含层的计算结果都与当前输入以及上一次的隐含层结果相关。
                        通过这种方法，RNN的计算结果便具备了记忆之前几次结果的特点。</div>
                    <div>&emsp;&emsp;LSTM的特点就是在RNN结构以外添加了各层的阀门节点。LSTM模型的记忆功能就是由这些阀门节点实现的。
                        当阀门打开的时候，前面模型的训练结果就会关联到当前的模型计算，而当阀门关闭的时候之前的计算结果就不再影响当前的计算。</div>
                    <div>&emsp;&emsp;因此，通过调节阀门的开关我们就可以实现早期序列对最终结果的影响。而当你不不希望之前结果对之后产生影响，
                        比如自然语言处理中的开始分析新段落或新章节，那么把阀门关掉即可。</div>
                </div>

            </el-container>

            <el-divider></el-divider>

            <el-row gutter="40">
                <el-col :span="12">
                    <el-card shadow="hover" class="mgb20" style="height:602px;">
                        <div slot="header" class="clearfix">
                            <span>训练loss图</span>
                            <i class="el-icon-s-data" style="padding-left: 20px"></i>
                        </div>


                        <div class="blocks" id="lossPicture">

                        </div>


                    </el-card>

                </el-col>

                <el-col :span="12">
                    <el-card shadow="hover" style="height:602px;">
                        <div slot="header" class="clearfix">
                            <span>拟合效果图</span>
                            <i class="el-icon-s-data" style="padding-left: 20px"></i>
                        </div>

                        <div class="blocks" id="fittingDiagram">

                        </div>

                    </el-card>


                </el-col>
            </el-row>

            <!--            <el-row gutter="40">-->
            <!--                <el-col :span="12">-->
            <!--                    <el-card shadow="hover" class="mgb20" style="height:600px;">-->
            <!--                        <div slot="header" class="clearfix">-->
            <!--                            <span>稳定段总推进力均值分析图</span>-->
            <!--                            <i class="el-icon-s-data" style="padding-left: 20px"></i>-->
            <!--                        </div>-->
            <!--                        <div style="height: 500px;width: 580px" id="myEchart1">-->

            <!--                        </div>-->
            <!--                    </el-card>-->

            <!--                </el-col>-->

            <!--                <el-col :span="12">-->
            <!--                    <el-card shadow="hover" style="height:600px;">-->
            <!--                        <div slot="header" class="clearfix">-->
            <!--                            <span>稳定段刀盘扭矩均值分析图</span>-->
            <!--                            <i class="el-icon-s-data" style="padding-left: 20px"></i>-->
            <!--                        </div>-->
            <!--                        <div style="height: 500px;width: 580px" id="myEchart2">-->

            <!--                        </div>-->

            <!--                    </el-card>-->


            <!--                </el-col>-->
            <!--            </el-row>-->

            <!--            <el-row gutter="40">-->
            <!--                <el-col :span="12" :offset="5">-->

            <!--                    <el-card shadow="hover" class="mgb20" style="height:600px;">-->

            <!--                        <div slot="header" class="clearfix">-->
            <!--                            <span>稳定段推进速度均值分析图</span>-->
            <!--                            <i class="el-icon-s-data" style="padding-left: 20px"></i>-->
            <!--                        </div>-->

            <!--                        <div style="height: 500px;width: 580px" id="myEchart3">-->

            <!--                        </div>-->

            <!--                    </el-card>-->

            <!--                </el-col>-->
            <!--            </el-row>-->

        </div>
    </div>
</template>

<script>

let lossData=[0.019891727715730667, 0.015867197886109352, 0.015630269423127174,
    0.015658920630812645, 0.01541389711201191, 0.015308316797018051,
    0.01528195571154356, 0.01517192181199789, 0.015274342149496078,
    0.015146018005907536, 0.01510472223162651, 0.015100996941328049,
    0.015081336721777916, 0.015164216980338097, 0.015067605301737785,
    0.015117057599127293, 0.015071132220327854, 0.015065873041749,
    0.015097319148480892, 0.015087896957993507, 0.015055240131914616,
    0.015085932798683643, 0.015066375024616718, 0.014966203831136227, 0.015013327822089195,
    0.015030964277684689, 0.01496599055826664, 0.01500732358545065, 0.014985148794949055,
    0.014898382127285004, 0.01488693617284298, 0.014915022999048233, 0.014834187924861908,
    0.014845781028270721, 0.01489992905408144, 0.014831620268523693, 0.014966988004744053,
    0.014958102256059647, 0.015155463479459286, 0.015122447162866592, 0.014979671686887741,
    0.014824559912085533, 0.014743134379386902, 0.014778241515159607, 0.014855501241981983,
    0.015034161508083344, 0.014876632951200008, 0.014908612705767155, 0.014995993115007877,
    0.014983235858380795, 0.01493958942592144, 0.015023997984826565, 0.01506007369607687,
    0.014908866956830025, 0.014926625415682793, 0.014929204247891903, 0.0148406270891428,
    .014761251397430897, 0.014771855436265469, 0.014719595201313496, 0.01484447717666626,
    0.01494482159614563, 0.014656522311270237, 0.014768368564546108, 0.014685412868857384,
    0.014888539910316467, 0.014668859541416168, 0.014721870422363281, 0.014816083945333958,
    0.014946559444069862, 0.014872650615870953, 0.01490148063749075, 0.014976207166910172,
    0.014871005900204182, 0.015104944817721844, 0.014732317067682743, 0.014863461256027222,
    0.01492043025791645, 0.014880993403494358, 0.014910238794982433, 0.014896349050104618,
    0.014870001934468746, 0.014813464134931564, 0.014729711227118969, 0.014757365919649601,
    0.014627259224653244, 0.014679763466119766, 0.014677468687295914, 0.01463653426617384,
    0.014629642479121685, 0.014673140831291676, 0.014636597596108913, 0.014696941711008549,
    0.014622082002460957, 0.014692648313939571, 0.014728769659996033, 0.014629754237830639,
    0.014721722342073917, 0.014635742641985416, 0.014635887928307056];
let fitData=[
    2942.392641,
    3013.518114,
    3179.002699,
    3119.361978,
    3172.595804,
    3013.220918,
    2657.163266,
    1370.768179,
    3200.057552,
    3066.926265,
    2762.575388,
    2401.740375,
    2537.502591,
    2496.993468,
    2486.013825,
    2855.320806,
    1487.854634,
    2079.444166,
    2526.25951,
    2648.677084,
    2713.286789,
    2686.083159,
    2418.772826,
    2350.9225,
    2375.652937,
    2575.204739,
    2336.235141,
    2525.973617,
    576.2750133,
    2406.651895,
    2277.794831,
    2288.848349,
    2469.981491,
    2544.826574,
    2635.261089,
    2797.267189,
    1646.657294,
    1110.967375,
    1241.120581,
    2386.21817,
    1674.166771,
    2097.560237,
    2309.42621,
    2980.382443,
    3085.392409,
    3071.832562,
    3024.163072,
    3003.447806,
    3106.42224,
    3060.831524,
    3042.487781,
    1968.719717,
    3051.230086,
    2967.770203,
    2706.574476,
    2833.705776,
    2715.69344,
    1792.923466,
    1441.391684,
    1614.874079,
    2958.24187,
    1885.999475,
    1657.692206,
    1535.733499,
    970.1307818,
    921.9848671,
    2245.002526,
    1662.025,
    1991.341081,
    2108.846097,
    2488.38385,
    2421.652915,
    3126.569765,
    3029.331418,
    3216.011397,
    2994.616129,
    2916.401263,
    2498.228155,
    2376.651211,
    2582.368156,
    855.5725556,
    1480.042469,
    1451.502192,
    3059.490711,
    3157.021953,
    3176.78407,
    3141.481154,
    2960.931007,
    2839.849488,
    3269.417317,
    2892.855119,
    2913.767423,
    3042.715488,
    3105.840989,
    3117.434622,
    3192.932519,
    3133.479089,
    2798.885122,
    2681.153483,
    2381.893417
];
let fitData1=[
    2880.938546,
    2997.375354,
    2517.061998,
    3413.381918,
    3224.498436,
    2890.581071,
    3015.421035,
    1456.816534,
    3018.013597,
    3022.644051,
    2843.800123,
    3012.146365,
    2823.337554,
    2895.118402,
    2633.778398,
    2807.11451,
    1876.407642,
    2102.155339,
    2486.013825,
    2855.320806,
    1846.287,
    2213.075,
    2526.25951,
    2648.677084,
    2713.286789,
    2686.083159,
    2418.772826,
    2350.9225,
    875.6529367,
    2575.204739,
    2336.235141,
    2525.973617,
    2525.973617,
    1991.341081,
    2108.846097,
    2488.38385,
    2421.652915,
    1526.569765,
    1407.11451,
    2576.407642,
    1102.155339,
    2486.013825,
    2855.320806,
    2487.854634,
    3079.444166,
    2826.25951,
    2648.677084,
    3235.733499,
    3270.130782,
    3321.984867,
    3042.487781,
    1968.719717,
    2833.778398,
    2807.11451,
    2876.407642,
    3102.155339,
    2486.013825,
    1855.320806,
    1487.854634,
    2079.444166,
    2526.25951,
    2648.677084,
    1535.733499,
    1970.130782,
    921.9848671,
    945.0025261,
    2662.025,
    1991.341081,
    2108.846097,
    2488.38385,
    2421.652915,
    3126.569765,
    3029.331418,
    3216.011397,
    2994.616129,
    2916.401263,
    2498.228155,
    3060.831524,
    2126.569765,
    2729.331418,
    916.0113968,
    1794.616129,
    1616.401263,
    2798.228155,
    3376.651211,
    2882.368156,
    3555.572556,
    2480.042469,
    2851.502192,
    3059.490711,
    3157.021953,
    3176.78407,
    3245.002526,
    2862.025,
    2991.341081,
    3108.846097,
    2788.38385,
    2421.652915,
    2843.800123,
    2512.146365

];



/**
 *
 */
let Xdata=[];
for(let i=1;i<=100;i++)
{
    Xdata.push(i);
}

export default {
    name: 'TNN',
    data() {
        return {
            optionLoss:{
                title: {
                    text: 'Loss图'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['训练集', '测试集']
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: Xdata
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '训练集',
                        type: 'line',

                        data: lossData
                    },
                    {
                        name: '测试集',
                        type: 'line',

                        data: lossData
                    },
                ]
            },

            optionFitting:{
                title: {
                    text: '拟合图'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['预测结果', '原数据']
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: Xdata
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '预测结果',
                        type: 'line',

                        data: fitData
                    },
                    {
                        name: '原数据',
                        type: 'line',

                        data: fitData1
                    },
                ]
            },

            option1:{
                xAxis: {
                    // \xB5	&#181;	&micro;	%B5	%C2%B5

                    type: 'value',
                    name: 'U'
                },
                yAxis: {
                    //\u2202	&#8706;	&part;	%u2202

                    type: 'value',
                    name: 'O'
                },
                series: [{
                    symbolSize: 20,
                    data: [
                        [10.0, 8.04],
                        [8.0, 6.95],
                        [13.0, 7.58],
                        [9.0, 8.81],
                        [11.0, 8.33],
                        [14.0, 9.96],
                        [6.0, 7.24],
                        [4.0, 4.26],
                        [12.0, 10.84],
                        [7.0, 4.82],
                        [5.0, 5.68]
                    ],
                    type: 'scatter'
                }]
            },

            tnnurl:require('@/assets/img/模型图-LSTM-AM.png'),
            srcList: [require('@/assets/img/模型图-LSTM-AM.png')],
            //     [
            //     '@/assets/img/模型图-tnn.png',
            //     // require('@/assets/img/模型图-tnn.png')
            // ],

            FittingDiagram:'https://i.postimg.cc/zDSjpbqw/Live-broadcast.jpg',
            LossDiagram:'https://i.postimg.cc/zDSjpbqw/Live-broadcast.jpg',
            fit:'scale-down',

            imgs3:require('@/assets/img/Loss1.png'),
            imgs4:require('@/assets/img/Loss2.png'),

        }
    },
    mounted() {

        // let myChart1=this.$echarts.init(document.getElementById('myEchart1'));
        // let myChart2=this.$echarts.init(document.getElementById('myEchart2'));
        // let myChart3=this.$echarts.init(document.getElementById('myEchart3'));

        let myChartLoss=this.$echarts.init(document.getElementById('lossPicture'));
        let myChartFitting=this.$echarts.init(document.getElementById('fittingDiagram'));

        // myChart1.setOption(this.option1);
        // myChart2.setOption(this.option1);
        // myChart3.setOption(this.option1);

        myChartLoss.setOption(this.optionLoss);
        myChartFitting.setOption(this.optionFitting);

    },
    methods(){

    }

};

</script>

<style scoped>


.el-image__inner{
    width: 100px;
    height: 100px;

    display: inline-block;
}

.el-image img{
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: 100%;
    display: block;
}


.blocks{
    height: 400px;
}

.demo-image__preview{
    /*display: grid;*/
    position: relative;
    padding-left: 250px;
    padding-top: 30px;
}

.el-header{
    background-color: #B3C0D1;
    font-size: 20px;
    line-height: 60px;
    align-content: center;
    font-weight: bolder;
    text-align: center;
}

.el-upload__text{
    width: 100px;
    height: 100px;
}

.el-card{
    background: #c7ddef;
}

.clearfix{
    font-weight: bolder;
}

.user-info {
    display: flex;
    align-items: center;

    border-bottom: 2px solid #ccc;

    font-weight:bolder;
}


.user-info-list {
    font-size: 14px;
    color: #999;
    line-height: 25px;
}

.user-info-list span {
    margin-left: 70px;
}

.mgb20 {
    margin-bottom: 20px;
}




</style>