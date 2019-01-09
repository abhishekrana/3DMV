import csv
import os

from laplotter import LossAccPlotter

input_dir = "/home/sk/windows/workspace/ADLCV/3DMV-colab/3dmv/logs/OverfitOnFourVolumetricGrids"
filesNames = ["log_train.csv", "log_scan_train.csv", "log_semantic_val.csv", "log_scan_val.csv"]


def read_loss_and_accuracy_from_csv(filenameIndex, skip_first_row=True):
    try:
        with open(os.path.join(input_dir, filesNames[filenameIndex]), mode='r') as infile:
            reader = csv.reader(infile)
            csv_data = []
            rows = list(reader)
            for row in rows:
                if skip_first_row:
                    skip_first_row = False
                    continue
                csv_data_row = []
                for i in range(len(row)):
                    item = row[i]
                    if item:
                        if i < 2:
                            csv_data_row.append(int(item))
                        else:
                            csv_data_row.append(float(item))
                csv_data.append(csv_data_row)
            return csv_data
    except FileNotFoundError as e:
        print(e)
        return []


def plot_image(title, filename, training, validation, train_vs_validation_iter_ratio):
    plotter = LossAccPlotter(title,
                             save_to_filepath=os.path.join(input_dir, filename),
                             show_regressions=False,
                             show_averages=True,
                             show_loss_plot=True,
                             show_acc_plot=True,
                             show_plot_window=False,
                             x_label="Iteration")
    # Store counter for next validation row to plot
    next_validation_row_index_to_plot = 0

    for row in range(len(training)):
        training_record = training[row]
        training_iter = training_record[1]
        loss_train = training_record[2]

        # Plot Both Training and Validation Record
        if len(validation) > next_validation_row_index_to_plot and \
                validation[next_validation_row_index_to_plot][1] <= training_iter / train_vs_validation_iter_ratio:
            val_record = validation[next_validation_row_index_to_plot]
            next_validation_row_index_to_plot = next_validation_row_index_to_plot + 1
            loss_val = val_record[2]
            if len(val_record) == 3:
                plotter.add_values(training_iter,
                                   loss_train=loss_train,
                                   loss_val=loss_val,
                                   redraw=False)
            elif len(val_record) > 3:
                inst_acc_val = val_record[3]
                inst_acc_train = training_record[4]
                plotter.add_values(training_iter,
                                   loss_train=loss_train,
                                   loss_val=loss_val,
                                   acc_train=inst_acc_train,
                                   acc_val=inst_acc_val,
                                   redraw=False)
        else:  # Plot Training Record only
            if len(training_record) == 3:
                plotter.add_values(training_iter,
                                   loss_train=loss_train,
                                   redraw=False)
            elif len(training_record) > 3:  # Valid value
                inst_acc_train = training_record[4]
                plotter.add_values(training_iter,
                                   loss_train=loss_train,
                                   acc_train=inst_acc_train,
                                   redraw=False)

    plotter.redraw()
    plotter.block()


# Plot for Semantic
training_semantic = read_loss_and_accuracy_from_csv(0)
validation_semantic = read_loss_and_accuracy_from_csv(2)

# Plot for Scan
training_scan = read_loss_and_accuracy_from_csv(1)
validation_scan = read_loss_and_accuracy_from_csv(3)

# LossAccPlotter uses equal iteration. Currently using
_train_vs_validation_iter_ratio = 1.0
plot_image('Semantic_Loss', "Semantic.jpg", training_semantic, validation_semantic, _train_vs_validation_iter_ratio)
plot_image('Scan_Loss', "Scan.jpg", training_scan, validation_scan, _train_vs_validation_iter_ratio)
