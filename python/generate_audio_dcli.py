from sensiml.dclproj.datasegmentsv2 import DataSegmentsV2, DataSegmentV2
from sensiml.dclproj import DCLProject
from typing import Optional
import os


def scale_values(original_len: int, new_len: int, original_value: int) -> int:
    scale_percent = original_value / original_len
    new_value = scale_percent * new_len
    return int(new_value)


def get_scaled_datasegments(
    pred_segments: DataSegmentsV2,
    original_size: int,
    scale_size: int,
    capture_name: str,
) -> DataSegmentsV2:

    scaled_datasegments = DataSegmentsV2()

    for segment in pred_segments:
        new_start = scale_values(
            original_size, scale_size, segment.capture_sample_sequence_start
        )
        new_end = scale_values(
            original_size, scale_size, segment.capture_sample_sequence_end
        )
        scaled_datasegments.append(
            DataSegmentV2(
                columns=segment.columns,
                segment_id=segment.segment_id,
                capture_sample_sequence_start=new_start,
                capture_sample_sequence_end=new_end,
                label_value=segment.label_value,
                uuid=segment.uuid,
                capture=capture_name,
            )
        )

    return scaled_datasegments


def generate_dcli(
    dcl_imu: DCLProject,
    dcl_audio: DCLProject,
    imu_session_import: str,
    imu_file_list: Optional[list] = None,
) -> DataSegmentsV2:

    if not imu_file_list:
        imu_file_list = dcl_imu.list_captures().name.values

    audio_file_list = dcl_audio.list_captures().name.values

    scaled_audio = DataSegmentsV2()
    for imu_file_name in imu_file_list:
        audio_file_name = imu_file_name.replace("imu", "audio").replace("csv", "wav")
        if audio_file_name not in audio_file_list:
            continue

        imu_segments = dcl_imu.get_capture_segments(
            imu_file_name, sessions=[imu_session_import]
        )
        audio_size = dcl_audio.get_capture_stats(audio_file_name)["number_samples"]
        imu_size = dcl_imu.get_capture_stats(imu_file_name)["number_samples"]
        scaled_audio.extend(
            get_scaled_datasegments(
                imu_segments, imu_size, audio_size - 1, audio_file_name
            )
        )

    return scaled_audio


if __name__ == "__main__":

    # SETTINGS
    PROJECT_DIR = None
    FILENAMES = []

    if not PROJECT_DIR:
        PROJECT_DIR = os.path.join(
            os.path.expanduser("~/"), "Documents", "SensiML", "Projects"
        )

    dclproj_imu_path = os.path.join(
        PROJECT_DIR, "Smart_Lock_IMU", "Smart_Lock_IMU.dclproj"
    )

    dclproj_audio_path = os.path.join(
        PROJECT_DIR, "Smart_Lock_Audio", "Smart_Lock_Audio.dclproj"
    )

    imu_session_import = "ground_truth"
    audio_session_export = "ground_truth"
    output_dcli = "scaled_segments.dcli"

    dcl_imu = DCLProject(path=dclproj_imu_path)
    dcl_audio = DCLProject(path=dclproj_audio_path)

    scaled_audio = generate_dcli(
        dcl_imu,
        dcl_audio,
        imu_session_import=imu_session_import,
        imu_file_list=FILENAMES,
    )

    dcli = scaled_audio.to_dcli(
        filename=output_dcli,
        session=audio_session_export,
    )
