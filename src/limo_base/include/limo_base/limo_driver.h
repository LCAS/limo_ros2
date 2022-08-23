/*
 * Copyright (c) 2021, Agilex Robotics
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its
 *    contributors may be used to endorse or promote products derived from
 *    this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef LIMO_DRIVER_H
#define LIMO_DRIVER_H

// C++
#include <thread>
#include <memory>
#include <atomic>

// ROS
#include "rclcpp/rclcpp.hpp"
#include <nav_msgs/msg/odometry.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <tf2_ros/transform_broadcaster.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <sensor_msgs/msg/imu.hpp>

// Limo
#include "limo_base/serial_port.h"
#include "limo_base/limo_protocol.h"
#include "limo_msgs/msg/limo_status.hpp"

namespace AgileX {
class LimoDriver : public rclcpp::Node {
 public:
  LimoDriver(const rclcpp::NodeOptions& options = rclcpp::NodeOptions());
  ~LimoDriver();

 private:
  // ----- ROS Node Parameters -----
  std::string port_name_;
  std::string odom_frame_;
  std::string base_frame_;
  std::string odom_topic_name_;
  bool pub_odom_tf_;
  bool use_mcnamu_;
  // ----- Internal Variables -----
  std::shared_ptr<SerialPort> port_;
  std::shared_ptr<std::thread> read_data_thread_;
  std::atomic<bool> keep_running_;

  ImuData imu_data_;
  uint8_t motion_mode_;  // current motion type

  static constexpr double max_inner_angle_ = 0.48869;  // 28 degree
  static constexpr double track_ = 0.172;    // m (left right wheel distance)
  static constexpr double wheelbase_ = 0.2;  // m (front rear wheel distance)
  static constexpr double left_angle_scale_ = 2.47;
  static constexpr double right_angle_scale_ = 2.47;

  double position_x_ = 0.0;
  double position_y_ = 0.0;
  double theta_ = 0.0;
  double present_theta_, last_theta_, delta_theta_, real_theta_, rad;
  bool flag = false;
  // ----- Subscribers & Publishers & Services -----
  std::shared_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
  rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr odom_publisher_;
  rclcpp::Publisher<limo_msgs::msg::LimoStatus>::SharedPtr status_publisher_;
  rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr imu_publisher_;
  rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr motion_cmd_sub_;
  // ----- Callbacks -----
  void twistCmdCallback(const geometry_msgs::msg::Twist::SharedPtr msg);

  bool ReadParameters();
  bool SetupHardware();
  bool SetupInterfaces();
  bool connect(std::string dev_name, uint32_t baudrate);
  void readData();
  void processRxData(uint8_t data);
  void parseFrame(const LimoFrame& frame);
  void sendFrame(const LimoFrame& frame);
  void setMotionCommand(double linear_vel, double steer_angle,
                        double lateral_vel, double angular_vel);
  void enableCommandedMode();
  void processErrorCode(uint16_t error_code);
  double normalizeAngle(double angle);
  double degToRad(double deg);
  double convertInnerAngleToCentral(double inner_angle);
  double convertCentralAngleToInner(double central_angle);
  void publishOdometry(double stamp, double linear_velocity,
                       double angular_velocity, double lateral_velocity,
                       double steering_angle);
  void publishLimoState(double stamp, uint8_t vehicle_state,
                        uint8_t control_mode, double battery_voltage,
                        uint16_t error_code, int8_t motion_mode);
  void publishIMUData(double stamp);
};  // LimoDriver
}  // namespace AgileX

#endif /* LIMO_DRIVER_H */
