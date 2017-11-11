#include "kalman_filter.h"
#include <iostream>
#include "math.h"

using Eigen::MatrixXd;
using Eigen::VectorXd;
using namespace std;

// Please note that the Eigen library does not initialize 
// VectorXd or MatrixXd objects with zeros upon creation.

KalmanFilter::KalmanFilter() {}

KalmanFilter::~KalmanFilter() {}

void KalmanFilter::Init(VectorXd &x_in, MatrixXd &P_in, MatrixXd &F_in,
                        MatrixXd &H_in, MatrixXd &R_in, MatrixXd &Q_in) {
  x_ = x_in;
  P_ = P_in;
  F_ = F_in;
  H_ = H_in;
  R_ = R_in;
  Q_ = Q_in;
}

void KalmanFilter::Predict() {
  x_ = F_ * x_;
  printf("pred:%f,%f,%f,%f\n",x_(0), x_(1), x_(2), x_(3));
  MatrixXd Ft = F_.transpose();
  P_ = F_ * P_ * Ft + Q_;  

}

void KalmanFilter::Update(const VectorXd &z) {
  VectorXd y = z - H_ * x_; //the error
  update_(y);
}

void KalmanFilter::UpdateEKF(const VectorXd &z) {
  //Cartesian coordinates to polar coordinates 
  float px = x_(0);
  float py = x_(1);
  float vx = x_(2);
  float vy = x_(3);

  double rho = sqrt(px*px + py*py);
  //printf("meas:%f,%f,%f\n",z(0),z(1),z(2));
  if (rho<0.00001) {
    cout << "rho is too small:" << rho <<"px:" << px <<"py:" << py;
    px += 0.001;
    py += 0.001;
    rho = sqrt(px*px + py*py);
  }
  //double phi = atan(py/px);
  double phi = atan2(py, px);
  double rho_dot = (px*vx + py*vy) / rho;
  VectorXd hx = VectorXd(3);
  hx << rho, phi, rho_dot;
  
  VectorXd y = z - hx; //error
  //Angle normalization
  //bool phi_adj_gt = y(1) > M_PI; 
  //bool phi_adj_lt = y(1) < -M_PI;
  //if (phi_adj_gt) {printf ("phi before adj:%f\n", y(1)); }
  while (y(1) > M_PI) {y(1) -= 2*M_PI;}
  //if (phi_adj_gt) {printf ("phi after gt adj:%f\n", y(1));}
  //if (phi_adj_lt) {printf ("phi before adj:%f\n", y(1)); }
  while (y(1) < -M_PI) {y(1) += 2*M_PI;}
  //if (phi_adj_lt) {printf ("phi after lt adj:%f\n", y(1));}
  update_(y);
}

void KalmanFilter::update_(const VectorXd &y) {
  MatrixXd Ht = H_.transpose();
  MatrixXd S = H_ * P_ * Ht + R_;
  MatrixXd Si = S.inverse();
  MatrixXd K =  P_ * Ht * Si;
  
  // New state
  x_ = x_ + (K * y);
  printf("new :%f %f %f %f\n", x_(0),x_(1),x_(2),x_(3));
  printf("----------------\n");
  long x_size = x_.size();
  MatrixXd I = MatrixXd::Identity(x_size, x_size);
  P_ = (I - K * H_) * P_; 
}
