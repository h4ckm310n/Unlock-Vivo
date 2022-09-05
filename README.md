# Unlock-Vivo
该Python脚本用于解锁Vivo手机的BL锁。MacOS 12.4（M1 MacBook Air）中测试过，其他环境不能确保能够正常运行。Vivo官方并不支持解锁，该操作也未必适用于所有机型，解锁有风险，操作须谨慎。

由于Vivo的骚操作，我们无法直接使用fastboot oem unlock命令来解锁。Vivo的解锁命令为fastboot vivo_bsp unlock_vivo，但是安卓官方的fastboot并不会识别这个命令，因此需要在fastboot的代码中添加一条else if条件并调用do_oem_command函数。XDA上也有大神编译了修改版（例如<https://forum.xda-developers.com/t/how-to-unlock-bootloader-of-vivo-phones.3686690/>）。

然而网上似乎并没有找到适用于MacOS的修改版fastboot的可执行文件，由于硬盘容量有限，本人也未能自行编译fastboot。受限于此，本人通过对fastboot进行usb抓包分析，并使用pyusb模拟fastboot对手机发包，来实现同等效果。解锁过程包括两部分，第一部分为刷vendor，第二部分为发送解锁命令。如果成功解锁，重启后手机会提示恢复出厂设置。代码中的FB_IDVENDOR和FB_IDPRODUCT分别为手机在fastboot模式下的厂商ID和产品ID，如有不同，请自行修改。
