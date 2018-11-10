import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse
from Base_agent import Agent
import cv2
from PIL import Image, ImageSequence
from keras import backend as K
from keras.models import Model
from keras.layers import Conv2D, Flatten, Dense, Lambda, Input, multiply

def plot_stats():
    abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Plot\\Plots-Certos")
    path_csv = [
        #"grayh8-full-reg-train-Doom-labyrinth.csv",
        # "errado-colorh8-train-Doom-labyrinth.csv",
        "DQN-Doom-labyrinth.csv",
        "grayh4-LSTM-train-Doom-labyrinth.csv",
        #"grayh8-train-Doom-labyrinth.csv",
                ]
    name = [
            #"Doom com histórico = 8-com regularização",
            #"Doom colorido histórico = 8",
            "DQN histórico = 4",
            #"Doom histórico = 8",
            "DRQN histórico = 4"
            ]
    colors = ["C{}".format(i) for i in range(10)]
    data_frame = []
    opt_classico = True
    opt_mean = True
    opt_window = 20
    epoch = 50000
    alpha = 0
    mean_fps = []
    leg_d= []
    for i, path in enumerate(path_csv):
        if (os.path.exists(os.path.join(abs_path, path))):
            dta = pd.read_csv(os.path.join(abs_path, path))
            # dta=dta.where(dta["Num_frames"]<=600000)
            data_frame.append(dta)
    for i, df in enumerate(data_frame):
        df_2 = df.rolling(window=opt_window, center=True).mean()
        print(df.mean())
        tim = df["Time"].sum()
        print("Número de frames treinados:{}".format(df["Num_frames"].max()))
        print("Tempo de treinamento:{:.2f} segundos".format(tim))
        print("Tempo de treinamento:{:.2f} horas".format(tim / 3600.0))
        plt.figure(1)
        if epoch == 1:
            plt.xlabel("Frames")
        else:
            plt.xlabel("Epochs (1 epoch = {} frames)".format(epoch))
        plt.ylabel("Valor médio de Q")
        plt.plot(df["Num_frames"] / epoch, df["Q_value"], color=colors[i], alpha=alpha)
        aux,=plt.plot(df_2["Num_frames"] / epoch, df_2["Q_value"], color=colors[i], label="{}".format(name[i]))
        leg_d.append(aux)
        plt.legend(handles=leg_d)
        plt.grid()
        plt.title("Valor médio da Q-function")

        plt.figure(2)
        plt.plot(df["Num_frames"] / epoch, df["Rewards"], color=colors[i], alpha=alpha)
        plt.plot(df_2["Num_frames"] / epoch, df_2["Rewards"], color=colors[i])
        if epoch == 1:
            plt.xlabel("Frames")
        else:
            plt.xlabel("Epochs (1 epoch = {} frames)".format(epoch))
        plt.ylabel("Reward médio por episódio")
        plt.legend(handles=leg_d)
        plt.grid()
        plt.title("Valor médio dos rewards recebidos")

        plt.figure(3)
        plt.plot(df["Num_frames"] / epoch, df["Loss"], color=colors[i], alpha=alpha)
        plt.plot(df_2["Num_frames"] / epoch, df_2["Loss"], color=colors[i])
        if epoch == 1:
            plt.xlabel("Frames")
        else:
            plt.xlabel("Epochs (1 epoch = {} frames)".format(epoch))
        plt.ylabel("Loss média por episódio")
        plt.legend(handles=leg_d)
        plt.grid()
        plt.title("Valor médio da Loss")

        plt.figure(4)
        plt.plot(df["Num_frames"], df["FPS"], color=colors[i], alpha=alpha)
        plt.plot(df_2["Num_frames"], df_2["FPS"], color=colors[i])
        plt.xlabel("Episódios")
        plt.ylabel("Frames/Segundo")
        plt.legend(handles=leg_d)
        plt.grid()
        plt.title("Desempenho em Frames/Segundo")
        mean_fps.append(df["FPS"].mean())
    plt.figure(5)
    plt.title("Frames/Segundo Médio")
    plt.bar(np.arange(len(mean_fps)), mean_fps, color=colors)
    for i,mean in enumerate(mean_fps):
        plt.text(x=(i)-0.1, y=mean/2.0, s="FPS médio:{:.2f}".format(mean),fontsize=14)
    plt.ylabel("Frames/Segundo")
    plt.xticks(np.arange(len(mean_fps)),name)
    plt.figure(1)
    plt.grid()
    plt.figure(2)
    plt.grid()
    plt.figure(3)
    plt.grid()
    plt.figure(4)
    plt.grid()
    plt.show()

def get_image_max_filter(model_input, layer_output, filter_index, input_shape, lr=100, iterations = 20,
                         input_img_data=np.array([])):
    """
    Function that finds the inputs that maximize the activation of the filters in different layers of the
    desired network. Based on the tutorial:
    How convolutional neural networks see the world. By Francois Chollet.
    https://blog.keras.io/how-convolutional-neural-networks-see-the-world.html

    :param model_input: Tensor.input
            Model's input as a tensor
    :param layer_output: Tensor.output
            The desired layer's output that contains the filter to be maximized
    :param filter_index: int
            Index of the filter to be maximized
    :param input_shape: tuple of int (Width, height, Depth)
            Input volume's shape that is fed to the model.
    :param lr:
            Training's Learning rate.
    :param iterations:
            Number of iterations that the algorithm will be trained.
    :return: tuple with:
            input_img_data : np.array (dtype=np.uint8)
                Image that maximizes the input filter.
            loss_vect : np.array float32
                History with the loss along the "training"
    """
    loss = K.mean(layer_output[:, :, :, filter_index])
    # compute the gradient of the input picture wrt this loss
    grads = K.gradients(loss, [model_input])[0]
    # normalization trick: we normalize the gradient
    grads /= (K.sqrt(K.mean(K.square(grads))) + 1e-5)
    # this function returns the loss and grads given the input picture
    iterate = K.function([model_input], [loss, grads])
    # we start from a gray image with some noise
    if input_img_data.shape[0]==0:
        input_img_data = np.random.random(input_shape) * 20 + 128.
    loss_vect = []
    print("iterations")
    # run gradient ascent for 20 steps
    for i in range(iterations):
        loss_value, grads_value = iterate([input_img_data])
        input_img_data += (np.clip(grads_value,-1,1))*127 * lr
        loss_vect.append(loss_value)

    return (deprocess_image(input_img_data), loss_vect)

def deprocess_image(img):
    """
    Function that normalize a image/tensor of dtype=float and convert to a RGB image
    dtype=np.uint8 with range of [0,255].

    :param img: np.array(dtype=float)
    :return: img : np.array(dtype=np.uint8)
    """
    # normalize tensor: center on 0., ensure std is 0.1
    img -= img.mean()
    img /= (img.std() + 1e-5)
    img *= 0.1
    # clip to [0, 1]
    img += 0.5
    img = np.clip(img, 0, 1)
    # convert to RGB array
    img *= 255
    img = np.clip(img, 0, 255).astype('uint8')

    return img

def get_rows_cols(num_elements):
    rows, cols = 0, 0
    # Exception to the rule
    if num_elements == 32:
        rows, cols = 4, 8
    # Trying to let rows and columns the closest possible
    else:
        cols = np.ceil(np.sqrt(num_elements)).astype(np.int)
        for i in range(cols,-1,-1):
            if cols * i < num_elements:
                rows = i+1
                break
    return (rows,cols)

def join_image(img , width_space=1, height_space=1):
    img_width, img_height, num_elements = img.shape[0], img.shape[1], img.shape[2]
    rows, cols = get_rows_cols(num_elements)
    total_width = (cols * (img_width + width_space)) + width_space  # +width_space for the last space
    total_height = (rows * (img_height + height_space)) + height_space
    new_img = Image.new('L', (total_width, total_height))
    for i in range(num_elements):
        idx, idy = np.unravel_index(i, (cols, rows), order="F")
        x_offset = (idx * (img_width + width_space)) + width_space
        y_offset = (idy * (img_height + height_space)) + height_space
        if img[:, :, i].dtype == np.float32:
            new_img.paste(Image.fromarray(deprocess_image(img[:, :, i]), mode="L"), (x_offset, y_offset))
        else:
            new_img.paste(Image.fromarray(img[:, :, i], mode="L"), (x_offset, y_offset))
    return new_img

def deconv_coord(conv_layer,layer_number,coord_x,coord_y):
    rect_width = 0
    rect_height = 0
    first_time = True
    # Calculating the rectangle's size and coordinates in the input image (deconvolving)
    for j in range(layer_number, -1, -1):
        strides = conv_layer[j].strides
        kernel_size = conv_layer[j].kernel_size
        # Calculating the padding
        W_1 = conv_layer[j].input_shape[1]
        W_2 = conv_layer[j].output_shape[1]
        padding = (W_2 * strides[0] + kernel_size[0] - strides[0] - W_1) / 2
        # Calculating the coordinates on the input image
        coord_x = int(coord_x * strides[0] - padding)
        coord_y = int(coord_y * strides[1] - padding)
        # size[-1] = F for the last layer, and size[-2]=(size[-1]-1)S + F1 for the previous ones to the last
        if first_time:
            first_time = False
            rect_width = kernel_size[0]
            rect_height = kernel_size[1]
        else:
            rect_width = (rect_width - 1) * strides[0] + kernel_size[0]
            rect_height = (rect_height - 1) * strides[1] + kernel_size[1]

    return (coord_x, coord_y,rect_width,rect_height)

def blend_img(frames, alpha=1.0, beta=0.6):
    bld_img = frames[0]
    for i in range(len(frames)-1):
        bld_img = cv2.addWeighted(frames[i+1],alpha,bld_img,beta,0)
    return bld_img

def get_convolutional_layers(agent):
    conv_layer = []
    conv_eval = []
    check_for_input = True
    conv_inputs = []
    for i in range(len(agent.Q_value.layers)):
        #Checks for all inputs that come before the first conv layer.
        if check_for_input and "input" in str(agent.Q_value.layers[i]):
            conv_inputs.append(agent.Q_value.layers[i].input)
        if "conv" in str(agent.Q_value.layers[i]):
            check_for_input = False
            conv_layer.append(agent.Q_value.layers[i])
            conv_eval.append(K.function(conv_inputs,[agent.Q_value.layers[i].output]))
    return (conv_layer,conv_eval)

def plot_network(agent,state_path,state_save):
    fig_idx = 0
    state=Image.open(state_path)
    frames =[np.array(frame.copy().getdata(),dtype=np.uint8).reshape(frame.size[1],frame.size[0],1)
                      for frame in ImageSequence.Iterator(state)]
    bld_img=blend_img(frames)
    fig0 = plt.figure(fig_idx)
    fig_idx += 1
    plt.imshow(bld_img.astype(np.uint8), cmap="gray_r")
    plt.imsave(os.path.join(state_save, "blended_img.png"), bld_img, cmap="gray_r")
    #=====================================================================================================#
    #    Gets each layer's activation and the portions of the input image that maximize its filters.
    #=====================================================================================================#
    state_vect = np.expand_dims(np.concatenate(frames, axis=2), axis=0)
    conv_layer,conv_eval = get_convolutional_layers(agent)
    for i in range(len(conv_layer)):
        img = np.squeeze(conv_eval[i]([state_vect])[0])
        num_elements = img.shape[2]
        fig1=plt.figure(fig_idx,figsize=(8,8))
        fig_idx+=1
        fig1.suptitle("Convolutional layer {}: Activations".format(i+1),fontsize=16)
        new_img = join_image(img)
        ax = plt.gca()
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_aspect('equal')
        ax.axis("off")
        plt.imshow(np.asarray(new_img,dtype=np.float32),cmap="gray")
        # Store the argmax, max and index of each filter
        argmax_vect = []
        max_vect = []
        filter_idx = []
        n_max = [20,3,3]
        # Case n_max has less elements than the number of layers
        while len(n_max) < len(conv_layer): n_max.append(1)
        for j in range(num_elements):
            img_cpy = img[:, :, j].copy()
            # Get n maximum elements of a filter
            # finds the first max and replace it for zero and repeat until it catch the n elements)
            for k in range(n_max[i]):
                arg_max = np.unravel_index(np.argmax(img_cpy), img_cpy.shape, order="C")
                argmax_vect.append(arg_max)
                max_vect.append(np.amax(img_cpy))
                img_cpy[arg_max] = 0.0
                filter_idx.append(j)
        fig1 = plt.figure(fig_idx, figsize=(8, 8))
        fig_idx += 1
        ax = plt.gca()
        filter_idx_max = []
        # Plotting the rectangles with the input parts that maximizes the activations of this layer.
        for k in range(n_max[i]):
            idx_max = int(np.argmax(max_vect))
            # Images uses (x,y) arrays uses (y,x)[rows,cols]
            ret_top_left = (argmax_vect[idx_max][1],argmax_vect[idx_max][0])
            max_vect[idx_max] = 0.0
            filter_idx_max.append(filter_idx[idx_max])
            coord_x, coord_y = ret_top_left[0] , ret_top_left[1]
            coord_x,coord_y,rect_width,rect_height = deconv_coord(conv_layer=conv_layer,layer_number=i,
                                                                  coord_x=coord_x,coord_y=coord_y)
            rect=patches.Rectangle((coord_x, coord_y), rect_width, rect_height, linewidth=1,
                                   edgecolor="red", facecolor='none',alpha=0.95)
            ax.add_patch(rect)

        ax.imshow(bld_img, cmap="gray_r")
        # ====================================================================================#
        #   Gets the input image that maximize each of the network`s filters
        # ====================================================================================#
        # print(filter_idx_max)
        # for i_aux in range(len(filter_idx_max)):
        #     for j in range(i_aux,len(filter_idx_max)-1):
        #         if filter_idx_max[i_aux] == -1:
        #             break
        #         if filter_idx_max[i_aux]==filter_idx_max[j+1]:
        #             filter_idx_max[j+1]=-1
        # filter_idx_max = [idx for idx in filter_idx_max if idx!=-1]
        # print(filter_idx_max)
        # n_idx = len(filter_idx_max)
        #fig1 = plt.figure(fig_idx, figsize=(8, 8))
        #fig_idx += 1
        #rows,cols = get_rows_cols(n_idx)
        #axes = [fig1.add_subplot(rows,cols,k+1) for k in range(n_idx)]
        # img_max = []
        # for j in range(num_elements):
        #     img_temp, loss = get_image_max_filter(model_input=agent.Q_value.layers[0].input,
        #                 layer_output=conv_layer[i].output, filter_index=j,
        #                 input_shape=state_vect.shape, )
        #     img_max.append(np.expand_dims(np.asarray(join_image(np.squeeze(img_temp))),axis=2))
        #     #axes[j].plot(range(len(loss)),np.array(loss))
        # fig1 = plt.figure(fig_idx, figsize=(8, 8))
        # fig_idx += 1
        # img_total = np.asarray(join_image(np.concatenate(img_max,axis=2),width_space=3,height_space=3))
        # print(img_total.shape)
        # im=plt.imshow(img_total,cmap="gray_r")._A
        # plt.imsave(os.path.join(state_save, "teste.png"), im, cmap="gray_r")


    #=====================================================================#
    #   Displaying the first layer's filters
    #=====================================================================#
    weights=agent.Q_value.get_weights()[0]
    n_filters = weights.shape[-1]
    fig2 = plt.figure(fig_idx,figsize=(4, 4))
    fig_idx +=1
    fig2.suptitle("First Convolutional Layer's filters", fontsize=16)
    filters_vec = []
    # joing each slice of a filter in one image
    for i in range(n_filters):
        filters_vec.append(np.expand_dims(join_image(np.squeeze(weights[:,:,:,i])),axis=2))
    # joining all the filters
    filter_total = np.squeeze(join_image(np.concatenate(filters_vec,axis=2),width_space=2,height_space=2))
    plt.imshow(filter_total,cmap="gray")
    ax = plt.gca()
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_aspect('equal')
    ax.axis("off")
    #==================================================================================================#
    #   Bar plot with the q-values
    #==================================================================================================#
    q_s = agent.Q_value.predict_on_batch([state_vect,agent.mask_one_e_greedy])
    fig2 = plt.figure(fig_idx, figsize=(4, 4))
    fig2.suptitle("Action-Values (Q) for each action available")
    fig_idx += 1
    coordx=np.arange(q_s.size)*0.8
    colors=["C{}".format(i) for i in range(q_s.size)]
    plt.bar(x=coordx,height=np.squeeze(q_s),color=colors)
    plt.xticks(coordx,agent.env.action_meanings())
    plt.ylabel("Action-Values (Q)")
    plt.xlabel("Actions (Buttons)")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot the RL-variables.")
    parser.add_argument("--mode", choices=["stats","network"], help="Mode to execute the plot",
                         required=True)
    parser.add_argument("--input_shape", default="84 84",
        help="Input frame's shape (WxHxColor_channel[if any]) that will be sent to the Neural Network. If "
        "just WxH are entered, the color_channel will be 1 (gray_scale)"
        "Type:str (with each argument separated by space or comma, and the whole sentence between quotation "
        "marks). Default:\"84 84\"")
    parser.add_argument("--history_size", default= 4, type=int,
        help="Number of sequential frames that will be stacked together to form the input volume to the NN. "
             "Type:int. Default:4")
    parser.add_argument("--load_weights", default= False, type=bool,
        help="Variable that controls if it's to load the weights from a external .h5 file generated by "
        "another simulation. Type:bool. Default (Train): False. Default(Test): True")
    parser.add_argument("--weights_load_path", default="",
        help="Path to .h5 file that contains the pre-treined weights. Default: None. REQUIRED IN PLOT NETWORK")
    parser.add_argument("--state", default="",
        help="Path to .gif file that contains the state to be plotted. Default: None. REQUIRED IN PLOT NETWORK")
    # args = parser.parse_args(["--mode","network","--load_weights", "True","--weights_load_path",
    #     "C:/Users/leozi/Reinforcement-Learning/Weights/Weights-certos/weights-PongNoFrameskip-v4-350000.h5",
    #     "--state",
    #     "C:/Users/leozi/Reinforcement-Learning/States/test-test-PongNoFrameskip-v4-Episode-1-State-428.gif"])
    args = parser.parse_args(["--mode","stats"])
    if args.mode.lower == "stats":
        plot_stats()
    else:
        if args.weights_load_path == "" and args.mode == "network":
            raise Exception("The path to load the weights was not valid!")
        dqn = Agent( input_shape=args.input_shape,
                        history_size=args.history_size,
                        load_weights=args.load_weights,
                        weights_load_path=args.weights_load_path,
                        silent_mode=True)
        plot_network(agent=dqn, state_path=args.state, state_save=dqn.path_save_plot)
