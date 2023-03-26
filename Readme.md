
## How to flash the firmware
1. Download the firmware file from the official Raspberry Pi Pico website.
2. Connect your Pico to your computer using a micro USB cable.
3. Put your Pico in bootloader mode by pressing and holding the BOOTSEL button while plugging in the USB cable
4. Your computer should recognize the Pico as a USB mass storage device.
5. Copy the firmware file to the Pico's mass storage device

```bash
cp -X Downloads/rp2-pico-w-20230323-unstable-v1.19.1-992-g38e7b842c.uf2 /Volumes/RPI-RP2/rp2-pico-w-20230323-unstable-v1.19.1-992-g38e7b842c.uf2
```

6. Once the file transfer is complete, unplug the USB cable from your computer. The Pico will automatically reboot and load the new firmware.