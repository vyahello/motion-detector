from datetime import datetime
import cv2
import numpy
import pandas


def counters(thresh_frame: numpy.ndarray) -> tuple:
    _counters, _ = cv2.findContours(
        thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    return _counters


def main() -> None:
    first_frame = None
    status_list = [None, None]
    times = []
    data_frame = pandas.DataFrame(columns=['Start', 'End'])
    video = cv2.VideoCapture(0)

    while True:
        check, frame = video.read()
        status = 0
        gray = cv2.GaussianBlur(
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (21, 21), 0
        )

        if first_frame is None:
            first_frame = gray
            continue

        delta_frame = cv2.absdiff(first_frame, gray)
        thresh_frame = cv2.dilate(
            cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1], None, 2
        )

        for count in counters(thresh_frame):
            if cv2.contourArea(count) < 1000:
                continue
            status = 1
            side_x, side_y, width, height = cv2.boundingRect(count)
            cv2.rectangle(
                frame,
                (side_x, side_y),
                (side_x + width, side_y + height),
                (0, 255, 0),
                3,
            )

        status_list.append(status)
        if status_list[-1] == 1 and status_list[-2] == 0:
            times.append(datetime.now())
        if status_list[-1] == 0 and status_list[-2] == 1:
            times.append(datetime.now())

        cv2.imshow('Gray Frame', gray)
        cv2.imshow('Delta Frame', delta_frame)
        cv2.imshow('Threshold Frame', thresh_frame)
        cv2.imshow('Color Frame', frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            if status == 1:
                times.append(datetime.now())
            break

    for iteration in range(0, len(times), 2):
        data_frame = data_frame.append(
            {'Start': times[iteration], 'End': times[iteration + 1]},
            ignore_index=True,
        )

    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
