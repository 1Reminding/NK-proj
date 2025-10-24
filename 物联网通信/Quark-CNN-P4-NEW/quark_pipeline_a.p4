/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>
#include "common/headers.p4"

#define REGISTER_SIZE 1

const bit<32> FLOW_ENTRIES = 1024;
const bit<32> IAT_limit = 32w9155273;

// 保持原有的宏定义
#define ADD_WEI_ACTION(x)\
    action add_wei_action_l1_##x(){multi_m1 = o_wei##x;}

#define ADD_MULTI_ACTION(x)\
    action add_multi_action_abcd_##x(){multi_m1 = o_wei##x; multi_m2 = hdr.hdr_metadata.ab_##x; multi_m3 = hdr.hdr_metadata.cd_##x;}\
    action add_multi_action_efgh_##x(){multi_m1 = o_wei##x; multi_m2 = hdr.hdr_metadata.ef_##x; multi_m3 = hdr.hdr_metadata.gh_##x;}\
    action add_multi_action_ababcd_##x(){multi_m1 = o_wei##x; multi_m2 = hdr.hdr_metadata.abcd_##x; multi_m3 = hdr.hdr_metadata.ab_##x;}

#define WRITE_RET_ACTION(x)\
    action write_ab_##x(){hdr.hdr_metadata.ab_##x = hdr.hdr_metadata.quan_temp_1;}\
    action write_cd_##x(){hdr.hdr_metadata.cd_##x = hdr.hdr_metadata.quan_temp_1;}\
    action write_ef_##x(){hdr.hdr_metadata.ef_##x = hdr.hdr_metadata.quan_temp_1;}\
    action write_gh_##x(){hdr.hdr_metadata.gh_##x = hdr.hdr_metadata.quan_temp_1;}\
    action write_abcd_##x(){hdr.hdr_metadata.abcd_##x = hdr.hdr_metadata.quan_temp_1;}

struct metadata {
    // BMv2 元数据结构
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/
parser MyParser(
    packet_in packet,
    out header_t hdr,
    inout metadata meta,
    inout standard_metadata_t standard_metadata) {
    
    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.ether_type) {
            ETHERTYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {//解析 IPv4 包头；根据协议类型判断是否继续解析 TCP；IP_PROTOCOLS_TCP 是常量，值为 6（即 TCP 协议）。
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol){
            IP_PROTOCOLS_TCP: parse_tcp;
            default: accept;
        }
    }

    state parse_tcp {//提取【TCP】头内容，然后跳转到自定义元数据提取。
       packet.extract(hdr.tcp);
       transition parse_meta;
    }

    state parse_meta {//提取自定义 header metadata；
        packet.extract(hdr.hdr_metadata);
        transition accept;//在 Quark 中，metadata 字段用于保存中间计算状态（如卷积输出、layer index、特征通道等）；
    }//最终 transition accept，表示 parser 结束，进入 pipeline 阶段。
}


/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/
control MyVerifyChecksum(inout header_t hdr, inout metadata meta) {
    apply { }
}          //Quark 不依赖 checksum 验证（为提高性能），因此这里是空实现；

/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

//推理核心逻辑
control MyIngress(
    inout header_t hdr,
    inout metadata meta,
    inout standard_metadata_t standard_metadata) {
    
    // 保持原有的变量定义
    int<8> multi_m1 = 0;
    int<8> multi_m2 = 0;    
    int<8> multi_m3 = 0;
    int<8> multi_m4 = 0;
    int<8> qi_zeropoint = 0;
    int<8> qo_zeropoint = 0;

    int<16> t_0 = 0;
    int<16> t_1 = 0;

    int<16> o_var1 = 0;
    int<16> o_var2 = 0;

    bit<2> multi_flag = 0;

    int<8> o_wei1 = 0;
    int<8> o_wei2 = 0;
    int<8> o_wei3 = 0;
    int<8> o_wei4 = 0;

    int<8> quan_ovar_1 = 0;
    int<8> quan_ovar_2 = 0;

    int<16> bias = 0;

    // maxpooling_tbl performs the maxpooling operations for the convolutional layers
    action greater(){ hdr.hdr_metadata.quan_temp_1 = quan_ovar_1; }
    action smaller(){ hdr.hdr_metadata.quan_temp_1 = quan_ovar_2; }
    table maxpooling_tbl{
        key = {
            quan_ovar_1 : exact;
            quan_ovar_2 : exact;
        }
        actions = {
            greater;
            smaller;
            NoAction;
        }
        default_action = greater;
        size = 10000;
    }//将较大的赋值到 hdr.hdr_metadata.quan_temp_1，用于后续写入 header 或继续推理

    // compare_ret_tbl performs argmax to retrieve the index and maximum element
    action ret_greater(){
        hdr.hdr_metadata.maxnum = hdr.hdr_metadata.quan_temp_1;
        hdr.hdr_metadata.result_index = hdr.hdr_metadata.channel_index;
    }

    //全连接层输出 argmax 得到最终分类结果
    table compare_ret_tbl{//compare_ret_tbl 表将逐个比较分类结果：如果当前 quan_temp_1 > maxnum，则：更新最大值 maxnum；
        key = {
            hdr.hdr_metadata.quan_temp_1 : exact;
            hdr.hdr_metadata.maxnum : exact;
        }
        actions = {//设置 result_index = 当前通道号；
            ret_greater;
            NoAction;
        }
        default_action = NoAction;//最终得到最大概率对应的类别（即 argmax）
        size = 10000;
    }

    // 权重加载,每个 CAP-Unit 执行一组卷积时会调用这个 Action，从表中加载对应通道的卷积核参数。
    action weight_act(int<8> w1, int<8> w2, int<8> w3, int<8> w4) {
        o_wei1 = w1;
        o_wei2 = w2;
        o_wei3 = w3;
        o_wei4 = w4;
    }

    //按照当前推理层级 level 和通道编号 channel_index 精确匹配；对应论文中 CAP-Unit 步骤 (i)：“加载权重”；控制面会用 table_add 指令下发这组匹配 → 权重写入。
    table weight_tbl{
        key = {
            hdr.hdr_metadata.level : exact;    
            hdr.hdr_metadata.channel_index : exact;
        }
        actions = {
            weight_act;
            NoAction;
        }
        default_action = NoAction;
        size = 32;
    }

    // 偏置加载，对应 CAP-Unit 步骤 (iv)：加偏置。
    action bias_act(int<16> w1) { bias = w1;}
    table bias_tbl{//同样以 level 和 channel_index 为索引；控制面下发所有 bias，数据面调用时即时加载。
        key = {
            hdr.hdr_metadata.level : exact;  
            hdr.hdr_metadata.channel_index : exact; 
        }
        actions = {
            bias_act;
            NoAction;
        }
        default_action = NoAction;
        size = 32;
    }

    // quanti_tbl and quanti_tbl_2 performs the (iv) quantization of convolutional layers
    action quanti_act(int<8> w_quan){ quan_ovar_1 = w_quan; }//w_quan 是从乘法和偏置累加后、经缩放系数乘变换后的结果；
    action quanti_default_act(){ quan_ovar_1 = -128; }//quan_ovar_1 被用于 ReLU/MaxPooling 等操作；
    table quanti_tbl{
        key = {
            o_var1: exact;
            hdr.hdr_metadata.level: exact;
        }
        actions = {
            quanti_act;
            quanti_default_act; //quanti_default_act() 是 fallback：当没有命中表项，返回极小值。
            NoAction;
        }
        size = 150000;
        default_action = quanti_default_act;
    }
//与上一个 quanti_tbl 配套使用的;对另一路卷积/特征通道的输出结果进行量化；便于与 quan_ovar_1 一起参与 MaxPooling 或比较。
    action quanti_act_2(int<8> w_quan){ quan_ovar_2 = w_quan; }
    table quanti_tbl_2{
        key = {
            o_var2: exact;
            hdr.hdr_metadata.level:exact;
        }
        actions = {
            quanti_act_2;
            quanti_default_act;
            NoAction;
        }
        size = 150000;
        default_action = quanti_default_act;
    }

    // 这两个量化表是专门为 FC 层（layer 4 和 layer 5）设计的。控制面提前计算并下发浮点转定点的查表映射。
    action quanti_act_l4(int<8> w_quan){ quan_ovar_1 = w_quan; }
    table quanti_tbl_l4{
        key = {
            o_var1: exact;
            hdr.hdr_metadata.channel_index : exact;
        }
        actions = {
            quanti_act_l4;
            quanti_default_act;
            NoAction;
        }
        size = 155000;
        default_action = quanti_default_act;
    }
    table quanti_tbl_l5{
        key = {
            o_var1: exact;
            hdr.hdr_metadata.channel_index : exact;
        }
        actions = {
            quanti_act_l4;
            quanti_default_act;
            NoAction;
        }
        size = 155000;
        default_action = quanti_default_act;
    }

    // 输出结果写回：get_level_X_tbl 表组（存储）
    WRITE_RET_ACTION(1)
    WRITE_RET_ACTION(2)
    WRITE_RET_ACTION(3)
    WRITE_RET_ACTION(4)
    table get_level_1_tbl{//用于 Layer 1 的输出保存；不同结果写入 ab_1 ~ gh_4 等字段；
    //最终用于下一次卷积或分类输入
        key = {
            hdr.hdr_metadata.result_index: exact;
            hdr.hdr_metadata.channel_index: exact;
        }
        actions = {
            write_ab_1;  write_ab_2;  write_ab_3;  write_ab_4;  
            write_cd_1;  write_cd_2;  write_cd_3;  write_cd_4;  
            write_ef_1;  write_ef_2;  write_ef_3;  write_ef_4;  
            write_gh_1;  write_gh_2;  write_gh_3;  write_gh_4;  NoAction;
        }
        size = 16;
        default_action = NoAction;
    }

    table get_level_2_tbl{//在这层引入了跨组融合或额外组合通道。
        key = {
            hdr.hdr_metadata.result_index: exact;
            hdr.hdr_metadata.channel_index: exact;
        }
        actions = {
            write_ab_1;  write_ab_2;  write_ab_3;  write_ab_4;  
            write_abcd_1;  write_abcd_2;  write_abcd_3;  write_abcd_4;  NoAction;
        }
        size = 16;
        default_action = NoAction;
    }

    table get_level_3_tbl{//支持根据当前层写入不同字段；动态调整写入目的字段，这可能与 stride=2 的下采样或跨层跳跃有关。
        key = {
            hdr.hdr_metadata.level: exact;
            hdr.hdr_metadata.channel_index: exact;
        }
        actions = {
            write_cd_1;  write_cd_2;  write_cd_3;  write_cd_4;  
            write_ab_1;  write_ab_2;  write_ab_3;  write_ab_4;  NoAction;
        }
        size = 16;
        default_action = NoAction;
    }

    table get_level_5_tbl{//最后一个存储表，对应输出或 argmax 前层；写入 softmax/logits 向量字段。
        key = {
            hdr.hdr_metadata.channel_index: exact;
        }
        actions = {
            write_cd_1;  write_cd_2;  write_cd_3;  write_cd_4;  
            write_ef_1;  write_ef_2;  write_ef_3;  write_ef_4;  
            write_gh_1;  write_gh_2;  write_gh_3;  write_gh_4;  
            write_abcd_1;  write_abcd_2;  write_abcd_3;  write_abcd_4;  NoAction;
        }
        size = 16;
        default_action = NoAction;
    }

    // add_multi_tbl：卷积单元输入选择器
    ADD_MULTI_ACTION(1)
    ADD_MULTI_ACTION(2)
    ADD_MULTI_ACTION(3)
    ADD_MULTI_ACTION(4)    
    table add_multi_tbl{
        key = {
            hdr.hdr_metadata.level: exact;
            hdr.hdr_metadata.result_index: exact;
            hdr.hdr_metadata.conv2_flag: exact;
        }
        actions = {
            add_multi_action_abcd_1;  add_multi_action_abcd_2;  add_multi_action_abcd_3;  add_multi_action_abcd_4;
            add_multi_action_efgh_1;  add_multi_action_efgh_2;  add_multi_action_efgh_3;  add_multi_action_efgh_4;
            add_multi_action_ababcd_1;  add_multi_action_ababcd_2;  add_multi_action_ababcd_3;  add_multi_action_ababcd_4;  NoAction;
        }
        size = 16;
        default_action = NoAction;
    }

    // add_multi_l1_tbl Assists in controlling the weights and features for computations in first unit layer
    action add_multi_action_l1_1(){multi_m2 = (int<8>)hdr.ipv4.diffserv; multi_m3 = (int<8>)hdr.ipv4.ttl;}    
    action add_multi_action_l1_2(){multi_m2 = hdr.hdr_metadata.gh_4; multi_m3 = hdr.hdr_metadata.abcd_1;}    
    action add_multi_action_l1_3(){multi_m2 = hdr.hdr_metadata.abcd_2; multi_m3 = hdr.hdr_metadata.abcd_3;}    
    action add_multi_action_l1_4(){multi_m2 = hdr.hdr_metadata.abcd_4; multi_m3 = hdr.hdr_metadata.maxnum;}
    table add_multi_l1_tbl{
        key = {
            hdr.hdr_metadata.result_index: exact;
        }
        actions = {
            add_multi_action_l1_1;
            add_multi_action_l1_2;
            add_multi_action_l1_3;
            add_multi_action_l1_4;
            NoAction;
        }
        size = 8;
        default_action = NoAction;
    }

    // add_multi_l1_tbl Assists in controlling the weights and features for computations in current fully connected unit
    action add_multi_action_l4_1(){ multi_m1 = o_wei1; multi_m2 = hdr.hdr_metadata.cd_1; multi_m4 = o_wei2; multi_m3 = hdr.hdr_metadata.cd_2;}
    action add_multi_action_l4_2(){ multi_m1 = o_wei3; multi_m2 = hdr.hdr_metadata.cd_3; multi_m4 = o_wei4; multi_m3 = hdr.hdr_metadata.cd_4;}
    action add_multi_action_l5_1(){ multi_m1 = o_wei1; multi_m2 = hdr.hdr_metadata.ab_1; multi_m4 = o_wei2; multi_m3 = hdr.hdr_metadata.ab_2;}
    action add_multi_action_l5_2(){ multi_m1 = o_wei3; multi_m2 = hdr.hdr_metadata.ab_3; multi_m4 = o_wei4; multi_m3 = hdr.hdr_metadata.ab_4;}
    table add_multi_l5_tbl{
        key = {
            hdr.hdr_metadata.level: exact;
            hdr.hdr_metadata.conv2_flag: exact;
        }
        actions = {
            add_multi_action_l4_1;
            add_multi_action_l4_2;
            add_multi_action_l5_1;
            add_multi_action_l5_2;
            NoAction;
        }
        size = 8;
        default_action = NoAction;
    }

    ADD_WEI_ACTION(1)
    ADD_WEI_ACTION(2)
    ADD_WEI_ACTION(3)
    ADD_WEI_ACTION(4)
    table add_wei_l1_tbl{
        key = {
            hdr.hdr_metadata.channel_index: exact;
        }
        actions = {
            add_wei_action_l1_1;
            add_wei_action_l1_2;
            add_wei_action_l1_3;
            add_wei_action_l1_4;
            NoAction;
        }
        size = 8;
        default_action = NoAction;
    }

    // 核心乘法操作表：multi_tbl_1 & multi_tbl_2
    action multi_act_1(int<16> w_quan){ t_0 = w_quan; }
    table multi_tbl_1{
        key = {
            multi_m1: exact;
            multi_m2: exact;
        }
        actions = {
            multi_act_1;
            NoAction;
        }
        size = 65536;
        default_action = NoAction;
    }
    action multi_act_2(int<16> w_quan){ t_1 = w_quan; }
    table multi_tbl_2{
        key = {
            multi_m1: exact;
            multi_m3: exact;
        }
        actions = {
            multi_act_2;
            NoAction;
        }
        size = 65536;
        default_action = NoAction;
    }

    apply{// 主体控制逻辑分为两个路径：
        // 1. 路径1：当 hdr.hdr_metadata.level == 1 时，执行以下操作
        // 2. 路径2：当 hdr.hdr_metadata.level != 1 时，执行以下操作

        standard_metadata.egress_spec = 1;
        /****************************************************************************************
        ******************* (ii) Retrive the weights and biases from the MATs *******************
        *****************************************************************************************/
        bias_tbl.apply();
        weight_tbl.apply();
        if(standard_metadata.ingress_port == 2){ // 替换 ig_intr_md.ingress_port
            standard_metadata.egress_spec = 2;
            hdr.hdr_metadata.recirculate = hdr.hdr_metadata.recirculate - 1;
            if(hdr.hdr_metadata.recirculate == 1){
                // 替换时间戳引用
                hdr.ethernet.dst_addr = (bit<48>)standard_metadata.ingress_global_timestamp;
                standard_metadata.egress_spec = 1;
            }
            /****************************************************************************************
            ************************* (i) Retrive the inputs from the header ************************
            *****************************************************************************************/
            if(hdr.hdr_metadata.level == 1){ 
                // The first CAP-UNit level of CNN
                add_multi_l1_tbl.apply();
                add_wei_l1_tbl.apply();
                multi_m2 = multi_m2 - qi_zeropoint;
                multi_m3 = multi_m3 - qi_zeropoint;
                hdr.hdr_metadata.ab_temp = 0;
                hdr.hdr_metadata.cd_temp = 0;
            }else if(hdr.hdr_metadata.level <= 3){
                // The remaining CAP-UNit levels of convolutional levels
                add_multi_tbl.apply();
                if(hdr.hdr_metadata.conv2_flag == 0){
                    hdr.hdr_metadata.ab_temp = 0;
                    hdr.hdr_metadata.cd_temp = 0;
                }
                hdr.hdr_metadata.conv2_flag = hdr.hdr_metadata.conv2_flag + 1;  
            }else if(hdr.hdr_metadata.level <= 5){
                // The fully connected CAP-Unit layers of CNN
                add_multi_l5_tbl.apply();
                if(hdr.hdr_metadata.conv2_flag == 0){
                    hdr.hdr_metadata.ab_temp = 0;
                    hdr.hdr_metadata.cd_temp = 0;
                }
                hdr.hdr_metadata.conv2_flag = hdr.hdr_metadata.conv2_flag + 2;
            }else{
                // CNN inference is completed.
                // hdr.hdr_metadata.result_index is the inference result
                // Operations that need to be performed on the inference results can be executed here...
            }
            
            /*****************************************************************************************
            ** (iii) Computing two sets of features and storing the accumulated convolution results **
            ******************************************************************************************/
            multi_tbl_1.apply();//定点乘法（CAP-Unit 步骤 (iii)）
            hdr.hdr_metadata.ab_temp = hdr.hdr_metadata.ab_temp + t_0;
            if(hdr.hdr_metadata.level >= 4){
                multi_m1 = multi_m4;
            }
            multi_tbl_2.apply();
            hdr.hdr_metadata.cd_temp = hdr.hdr_metadata.cd_temp + t_1;
            
            // When all channels have been accumulated, proceed with steps (iv)~(vii)
            if(hdr.hdr_metadata.conv2_flag == 4){
                hdr.hdr_metadata.conv2_flag = 0;

                /****************************************************************************************
                ***************************** (iv) Quantize accumulation results ************************
                *****************************************************************************************/
                if(hdr.hdr_metadata.level < 4){
                    o_var1 = hdr.hdr_metadata.ab_temp + bias;
                    o_var2 = hdr.hdr_metadata.cd_temp + bias;

                    quanti_tbl.apply();
                    quanti_tbl_2.apply();

                    /****************************************************************************************
                    ************************************* (v) ReLU module ***********************************
                    *****************************************************************************************/
                    if(quan_ovar_1 < 0){
                        quan_ovar_1 = 0;
                    }
                    if(quan_ovar_2 < 0){
                        quan_ovar_2 = 0;
                    }

                    /****************************************************************************************
                    ********************************* (vi) Maxpooling module ********************************
                    *****************************************************************************************/
                    maxpooling_tbl.apply();
                }else if(hdr.hdr_metadata.level == 4){
                    // Fully connected layers 1
                    /****************************************************************************************
                    ******************************** (iv)~(v) Quantize and ReLU *****************************
                    *****************************************************************************************/
                    o_var1 = hdr.hdr_metadata.ab_temp + hdr.hdr_metadata.cd_temp; 
                    quanti_tbl_l4.apply();
                    if(quan_ovar_1 < 0){
                        quan_ovar_1 = 0;
                    }
                    hdr.hdr_metadata.quan_temp_1 = quan_ovar_1;
                }else{
                    // Fully connected layers 2
                    /****************************************************************************************
                    ******************************** (iv)~(v) Quantize and ReLU *****************************
                    *****************************************************************************************/
                    o_var1 = hdr.hdr_metadata.ab_temp + hdr.hdr_metadata.cd_temp; 
                    quanti_tbl_l5.apply();
                    if(quan_ovar_1 < 0){
                        quan_ovar_1 = 0;
                    }
                    hdr.hdr_metadata.quan_temp_1 = quan_ovar_1;
                }
        
                /****************************************************************************************
                ************************************* (iv) Storage outputs ******************************
                *****************************************************************************************/
                if(hdr.hdr_metadata.level == 1){
                    get_level_1_tbl.apply();
                    hdr.hdr_metadata.conv2_flag = 4;
                    if(hdr.hdr_metadata.channel_index == 4){
                        hdr.hdr_metadata.channel_index = 0;
                        hdr.hdr_metadata.result_index = hdr.hdr_metadata.result_index + 1;
                        if(hdr.hdr_metadata.result_index == 5){
                            hdr.hdr_metadata.result_index = 1;
                            hdr.hdr_metadata.level = 2;
                            hdr.hdr_metadata.conv2_flag = 0;
                        }
                    }
                }else if(hdr.hdr_metadata.level == 2){
                    get_level_2_tbl.apply();
                    if(hdr.hdr_metadata.channel_index == 4){
                        hdr.hdr_metadata.channel_index = 0;
                        hdr.hdr_metadata.result_index = hdr.hdr_metadata.result_index + 1;
                        if(hdr.hdr_metadata.result_index == 3){
                            hdr.hdr_metadata.result_index = 1;
                            hdr.hdr_metadata.level = 3;
                        }
                    }
                }else if(hdr.hdr_metadata.level <= 4){
                    get_level_3_tbl.apply();
                    if(hdr.hdr_metadata.channel_index == 4){
                        hdr.hdr_metadata.channel_index = 0;
                        hdr.hdr_metadata.level = hdr.hdr_metadata.level + 1;
                        hdr.hdr_metadata.maxnum = 0;
                    }                    
                }else if(hdr.hdr_metadata.level == 5){
                    // compare_ret_tbl performs argmax to retrieve the index and maximum element
                    // the index will be stored in hdr.hdr_metadata.result_index
                    // the maximum output will be stored in hdr.hdr_metadata.maxnum
                    compare_ret_tbl.apply();
                    get_level_5_tbl.apply();
                    if(hdr.hdr_metadata.channel_index == 15){
                        hdr.hdr_metadata.channel_index = 0;
                        hdr.hdr_metadata.level = 6;    
                        hdr.hdr_metadata.recirculate = 1;  
                        standard_metadata.egress_spec = 1;   // 替换 ig_tm_md.ucast_egress_port = 65
                        hdr.ethernet.dst_addr = (bit<48>)standard_metadata.ingress_global_timestamp; // 替换 ig_intr_md.ingress_mac_tstamp
                    }                    
                }
                hdr.hdr_metadata.channel_index = hdr.hdr_metadata.channel_index + 1;
            }
        }else{
            // 初始化控制参数
            hdr.hdr_metadata.level = 1;
            hdr.hdr_metadata.channel_index = 1;
            hdr.hdr_metadata.conv2_flag = 4;
            hdr.hdr_metadata.result_index = 1;
            hdr.hdr_metadata.recirculate = 105;
            
            hdr.ethernet.src_addr = (bit<48>)standard_metadata.ingress_global_timestamp;
            standard_metadata.egress_spec = 2;
        }
        # ig_tm_md.bypass_egress = (bit<1>)true;
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/
control MyEgress(
    inout header_t hdr,
    inout metadata meta,
    inout standard_metadata_t standard_metadata) {
    apply { }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/
control MyComputeChecksum(inout header_t hdr, inout metadata meta) {
    apply {
        update_checksum(
            hdr.ipv4.isValid(),
            { hdr.ipv4.version,
              hdr.ipv4.ihl,
              hdr.ipv4.diffserv,
              hdr.ipv4.total_len,
              hdr.ipv4.identification,
              hdr.ipv4.flags,
              hdr.ipv4.frag_offset,
              hdr.ipv4.ttl,
              hdr.ipv4.protocol,
              hdr.ipv4.src_addr,
              hdr.ipv4.dst_addr },
            hdr.ipv4.hdr_checksum,
            HashAlgorithm.csum16);
    }
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/
control MyDeparser(packet_out packet, in header_t hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
        packet.emit(hdr.hdr_metadata);
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/
V1Switch(
    MyParser(),
    MyVerifyChecksum(),
    MyIngress(),
    MyEgress(),
    MyComputeChecksum(),
    MyDeparser()
) main;
