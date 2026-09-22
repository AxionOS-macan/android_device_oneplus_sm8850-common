#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/oneplus/sm8850-common',
    'hardware/oplus',
    'hardware/qcom-caf/sm8850',
    'hardware/qcom-caf/wlan',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'libolc_vnd',
        'libosensenativeproxy_client',
        'libPanelChaplin',
        'libpwirisfeature',
        'vendor.pixelworks.hardware.display@1.0',
        'vendor.pixelworks.hardware.display@1.1',
        'vendor.pixelworks.hardware.display@1.2',
        'vendor.pixelworks.hardware.feature@1.0',
        'vendor.pixelworks.hardware.feature@1.1',
        'vendor.qti.ImsRtpService-V2-ndk',
        'vendor.qti.diaghal-V1-ndk',
        'vendor.qti.hardware.dpmaidlservice-V1-ndk',
        'vendor.qti.hardware.wifidisplaysession_aidl-V1-ndk',
        'vendor.qti.qccsyshal_aidl-V1-ndk',
        'vendor.qti.qccvndhal_aidl-V1-ndk',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    'odm/bin/hw/vendor.oplus.hardware.biometrics.fingerprint@2.1-service_uff': blob_fixup()
        .add_needed('libshims_aidl_fingerprint_v3.oplus.so'),
    (
        'odm/bin/hw/vendor-oplus-hardware-touch-V2-hbp5-service',
        'odm/bin/hw/vendor.oplus.hardware.biometrics.fingerprint@2.1-service_uff',
        'odm/bin/touchDaemon',
        'odm/lib64/libdisplayfossfeature_nature.so',
        'odm/lib64/libstc_color_feature.so',
        'vendor/bin/hw/audiohalservice.qti',
        'vendor/bin/hw/vendor.qti.hardware.display.composer-service',
        'vendor/bin/qvrdatauploader',
        'vendor/lib64/hw/libaudioeffecthal.qti.so',
        'vendor/lib64/libsdmclient.so',
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v36.so'),
    'odm/etc/gps.conf': blob_fixup()
        .binary_regex_replace(b'com.oplus.locationproxy', b'com.google.android.carrierlocation')
        .binary_regex_replace(b'DEBUG_LEVEL = 3', b'DEBUG_LEVEL = 2'),
    'odm/etc/init/init.network.rc': blob_fixup()
        .regex_replace(r'/\* (Huo\.Chen@SYSTEM\.RF, 2024/09/06, Add for ICC) \*/', r'# \1'),
    'odm/etc/izat.conf': blob_fixup()
        .regex_replace(r'(PROCESS_NAME=xtra-daemon\nPROCESS_ARGUMENT=\nPROCESS_STATE=)ENABLED', r'\1DISABLED'),
    'product/etc/sysconfig/com.android.hotwordenrollment.common.util.xml': blob_fixup()
        .regex_replace('/my_product', '/product'),
    'vendor/etc/init/vendor.dpmd.rc': blob_fixup()
        .regex_replace(
            r'(    group system readproc inet radio wakelock oem_2901\n)(    disabled)',
            r'\1    interface aidl vendor.qti.hardware.dpmaidlservice.IDpmService/default\n\2',
        ),
    'system_ext/bin/horae': blob_fixup()
        .replace_needed('libprotobuf-cpp-lite.so', 'libprotobuf-cpp-lite-21.12.so'),
    (
        'system_ext/etc/seccomp_policy/tcmd.policy',
        'vendor/etc/seccomp_policy/qsap_qapeservice.policy',
        'vendor/etc/seccomp_policy/syshealthmon.policy'
    ): blob_fixup()
        .add_line_if_missing('lseek: 1'),
    'system_ext/lib64/libwfdnative.so': blob_fixup()
        .add_needed('libinput_shim.so'),
    'vendor/bin/vendor_modprobe.sh': blob_fixup()
        .regex_replace(r'\n.*OPLUS_FEATURE_WIFI_FTM[\s\S]*?OPLUS_FEATURE_WIFI_FTM.*\n', ''),
    # Replace the vendor audio include with Dolby Vision in each canoe variant.
    (
        'vendor/etc/media_codecs_canoe_sku1.xml',
        'vendor/etc/media_codecs_canoe_sku2.xml',
        'vendor/etc/media_codecs_canoe_sku3.xml',
        'vendor/etc/media_codecs_canoe_v1.xml',
        'vendor/etc/media_codecs_canoe_v2.xml',
        'vendor/etc/media_codecs_canoe_v3.xml',
    ): blob_fixup()
        .regex_replace('.*media_codecs_(google_audio|google_c2|google_telephony|google_video).*\n', '')
        .regex_replace('media_codecs_vendor_audio', 'media_codecs_dolby_vision'),
    (
        'vendor/lib64/hw/android.hardware.bluetooth.audio_sw.so',
        'vendor/lib64/hw/libaudiocorehal.default.so',
        'vendor/lib64/hw/libaudiocorehal.qti.so',
        'vendor/lib64/libaudioplatformconverter.qti.so',
        'vendor/lib64/libaudioserviceexampleimpl.so',
        'vendor/lib64/libqtigefar.so',
        'vendor/lib64/libwfdmmsrc_proprietary.so',
    ): blob_fixup()
        .replace_needed('android.hardware.audio.core-V3-ndk.so', 'android.hardware.audio.core-V4-ndk.so'),
    (
        'vendor/lib64/hw/android.hardware.bluetooth.audio_sw.so',
        'vendor/lib64/hw/libaudiocorehal.qti.so',
        'vendor/lib64/hw/libaudioeffecthal.qti.so',
        'vendor/lib64/libaudioserviceexampleimpl.so',
        'vendor/lib64/libqtigefar.so',
        'vendor/lib64/soundfx/libqcompostprocbundle.so',
        'vendor/lib64/soundfx/libqcomvisualizer.so',
        'vendor/lib64/soundfx/libqcomvoiceprocessing.so',
    ): blob_fixup()
        .replace_needed('android.media.audio.common.types-V5-ndk.so', 'android.media.audio.common.types-V4-ndk.so'),
    'vendor/lib64/libaudioserviceexampleimpl.so': blob_fixup()
        .add_needed('libaudioutils_shim.so')
        .add_needed('libbluetooth_audio_session_aidl_shim.so'),
    (
        'vendor/lib64/libcwb_qcom_aidl.so',
        'vendor/lib64/libhwcsensor.so',
        'vendor/lib64/libsdmclient.so',
    ): blob_fixup()
        .replace_needed('vendor.qti.hardware.display.config-V11-ndk.so', 'vendor.qti.hardware.display.config-V13-ndk.so'),
    (
        'vendor/lib64/libpwirishalwrapper.so',
        'vendor/lib64/libqcodec2_core.so',
        'vendor/lib64/libsdmclient.so',
    ): blob_fixup()
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    'vendor/lib64/libpwirishalwrapper.so': blob_fixup()
        .replace_needed('android.hardware.graphics.composer3-V3-ndk.so', 'android.hardware.graphics.composer3-V4-ndk.so'),
    'vendor/lib64/libsdmcore.so': blob_fixup()
        .binary_regex_replace(
            b'/my_product/vendor/etc/display_apollo_list.xml',
            b'/vendor/etc/oplus_disp/display_apollo_list.xml',
        )
        .binary_regex_replace(
            b'/my_product/vendor/etc/display_apollo_list_',
            b'/vendor/etc/oplus_disp/display_apollo_list_',
        )
        .binary_regex_replace(
            b'/my_product/vendor/etc/',
            b'/vendor/etc/oplus_disp/',
        )
        .add_needed('libbase.so'),
    'vendor/usr/keylayout/gpio-keys.kl': blob_fixup()
        .add_line_if_missing('key 735   ASSIST'),
    'vendor/etc/public.libraries.txt': blob_fixup()
        .add_line_if_missing('libarcsoft_hdr_couple_api.so')
        .add_line_if_missing('libarcsoft_high_dynamic_range_couple.so')
        .add_line_if_missing('libarcsoft_smart_denoise.so')
        .add_line_if_missing('libarcsoft_turbo_hdr_raw.so')
        .add_line_if_missing('libarcsoft_turbo_raw.so')
        .add_line_if_missing('libarcsoft_qnnhtp.so')
        .add_line_if_missing('libQnnHtp.so')
        .add_line_if_missing('libQnnSystem.so')
        .add_line_if_missing('libQnnHtpV81Stub.so')
        .add_line_if_missing('libQnnGpu.so'),
    'vendor/etc/perf/perfboostsconfig.xml': blob_fixup()
        .regex_replace(r'Enable="false"', r'Enable="true"'),
    'vendor/etc/sensors/hals.conf': blob_fixup()
        .regex_replace(r'sensors\.qsh\.so', 'sensors.fusionlight.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm8850-common',
    'oneplus',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)
module.add_proprietary_file('proprietary-files-phone.txt').add_copy_files_guard(
    'TARGET_IS_TABLET', 'true', invert=True
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
