#include "TabuaMDT.hpp"

double qx2qxj(double qx1, double qx2, double qx3)
{
	return qx1 * (1 - 0.5 * (qx2 + qx3) + 1.0 / 3.0 * (qx2 * qx3));
}

std::vector<double> qx2qxj(std::vector<double> qx1, std::vector<double> qx2, std::vector<double> qx3)
{
	std::vector<double> qxj;
	qxj.reserve(qx1.size());
	for (int i = 0; i < qx1.size(); i++)
	{
		qxj.push_back(qx2qxj(qx1[i], qx2[i], qx3[i]));
	}
	return qxj;
}

std::vector<double> converter_mdt(std::vector<double> qx) {
	std::vector<double> qxj(3);
	int tamanho = 3 - qx.size();
	double zeros = 0.0;
	if (tamanho < 0) {
		throw std::invalid_argument("O número de tábuas não pode ser maior que 3");
	}
	for (int i = 0; i < tamanho; i++) {
		qx.push_back(zeros);
	}
	qxj[0] = qx2qxj(qx[0], qx[1], qx[2]);
	qxj[1] = qx2qxj(qx[1], qx[2], qx[0]);
	qxj[2] = qx2qxj(qx[2], qx[0], qx[1]);
	return qxj;
}

std::vector<std::vector<double>> converter_mdt(std::vector<std::vector<double>> qx) {
	std::vector<std::vector<double>> qxj(3);
	int tamanho = 3 - qx.size();
	std::vector<double> zeros(qx[0].size(), 0.0);
	if (tamanho < 0) {
		throw std::invalid_argument("O número de tábuas não pode ser maior que 3");
	}
	for (int i = 0; i < tamanho; i++) {
		qx.push_back(zeros);
	}
	qxj[0] = qx2qxj(qx[0], qx[1], qx[2]);
	qxj[1] = qx2qxj(qx[1], qx[2], qx[0]);
	qxj[2] = qx2qxj(qx[2], qx[0], qx[1]);
	return qxj;
}