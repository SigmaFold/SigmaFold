clc; clear; close all

fov_half_data = readmatrix("tensorboard_placing_fov_half.csv");
fov1_data = readmatrix("tensorboard_placing_fov1.csv");
fov2_data = readmatrix("tensorboard_placing_fov2.csv");

fov_array = {fov_half_data, fov1_data, fov2_data};
color_array = {[0 0.4470 0.7410], [0.8500 0.3250 0.0980], [0.9290 0.6940 0.1250]};

i=1;
for data=fov_array
    n = 10; % filter order
    episodes = data{1}(2:end,2);
    ep_len_raw = data{1}(2:end, 3);
    ep_len_ma = filter(ones(n, 1)/n, 1, ep_len_raw);
    nb_data_points = numel(ep_len_raw);
    disp(color_array{i})

    bin_size = 10;
    max_bound=[];
    min_bound=[];
    
    for j = 1:bin_size:nb_data_points-bin_size
        temp = ep_len_raw(j:j+bin_size);
        max_bound(end+1) = max(temp);
        min_bound(end+1) = min(temp);
    end
    size_bounds = numel(max_bound);
    n=2;
    max_bound = filter(ones(n, 1)/n, 1, max_bound);
    min_bound = filter(ones(n, 1)/n, 1, min_bound);

    figure(1); hold on;
    x_ax = linspace(episodes(1), episodes(end), size_bounds);
    x2 = [x_ax, fliplr(x_ax)];
    inBetween = [min_bound, fliplr(max_bound)];
    fill(x2, inBetween,color_array{i}, FaceAlpha=0.5, EdgeAlpha=0, HandleVisibility="off");

    plot(episodes, ep_len_ma, Color=[color_array{i}], LineWidth=1)
%     plot(episodes, ep_len_raw, Color=[color_array{i}, 0.5],LineWidth=1, HandleVisibility="off")
    i = i + 1;
end
legend(["FoV=0.5", "FoV=1", "FoV=5"], Interpreter="tex");
xlabel("Episode Index")
xticks([0, 1e5 2e5 3e5 4e5 5e5 6e5, 7e5])
xticklabels({'0', '100k','200k','300k','400k','500k','600k', '700k' })
ylabel("Average Reward per Episode")
xlim([0, 3.5e5])


































