// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract InsuranceClaim {
    address admin;

    constructor() {
        admin = msg.sender;
    }

    struct UserDetails {
        address _wallet;
        string _insuranceType;
        string _policyId;
        string _adharNumber;
        string _phoneNumber;
        bool _exist;
        string _status;
    }

    mapping(address => UserDetails) userDetails;
    address[] userAddresses;

    struct NomineeDetails {
        address _wallet;
        string _nomineeName;
        string _nomineeAdhar;
        string _nomineePhoneNumber;
        bool _exist;
    }

    mapping(address => NomineeDetails) nomineeDetails;
    address[] nomineeAddresses;

    struct BankDetails {
        address _wallet;
        string _bankName;
        string _accountNumber;
        string _ifscCode;
        bool _exist;
    }

    mapping(address => BankDetails) bankDetails;
    address[] bankAddresses;

    struct certificateDetails {
        address _wallet;
        string _policyPaperPath;
        string _policyPaperHash;
        string _reportPaperPath;
        string _reportPaperHash;
        bool _exist;
    }

    mapping(address => certificateDetails) certificates;
    address[] certificateAddresses;

    struct PoliceDetails{
      address _wallet;
      string _policyId;
      string _policeName;
      string _policeContactNumber;
      string _policeFIRPath;
      string _policeFIRHash;
      bool _exist;
    }

    mapping(address => PoliceDetails) policeDetails;
    address[] policeAddresses;

    struct HospitalDetails{
      address _wallet;
      string _policyId;
      string _doctorName;
      string _doctorContactNumber;
      string _doctorreportPath;
      string _doctorreportHash; 
      bool _exist;
    }

    mapping(address => HospitalDetails) hospitalDetails;
    address[] hospitalAddresses;

    // UserDetails Functions
    function addUserDetails(
        address wallet,
        string memory insuranceType,
        string memory policyId,
        string memory adharNumber,
        string memory phoneNumber
    ) public {
        require(!userDetails[wallet]._exist, "Details Already Existed");

        UserDetails memory new_user = UserDetails(wallet, insuranceType, policyId, adharNumber, phoneNumber, true,"Pending");
        userDetails[wallet] = new_user;
        userAddresses.push(wallet);
    }

    function viewUserDetailsByWallet(address wallet) public view returns (UserDetails memory) {
        require(userDetails[wallet]._exist, "No record with this wallet");
        return userDetails[wallet];
    }

    function viewAllUserDetails() public view returns (UserDetails[] memory) {
        UserDetails[] memory userArray = new UserDetails[](userAddresses.length);

        for (uint i = 0; i < userAddresses.length; i++) {
            userArray[i] = userDetails[userAddresses[i]];
        }
        return userArray;
    }

    // NomineeDetails Functions
    function addNomineeDetails(
        address wallet,
        string memory nomineeName,
        string memory nomineeAdhar,
        string memory nomineePhoneNumber
    ) public {
        require(!nomineeDetails[wallet]._exist, "Details Already Existed");

        NomineeDetails memory new_nominee = NomineeDetails(wallet, nomineeName, nomineeAdhar, nomineePhoneNumber, true);
        nomineeDetails[wallet] = new_nominee;
        nomineeAddresses.push(wallet);
    }

    function viewNomineeDetailsByWallet(address wallet) public view returns (NomineeDetails memory) {
        require(nomineeDetails[wallet]._exist, "No record with this wallet");
        return nomineeDetails[wallet];
    }

    function viewAllNomineeDetails() public view returns (NomineeDetails[] memory) {
        NomineeDetails[] memory nomineeArray = new NomineeDetails[](nomineeAddresses.length);

        for (uint i = 0; i < nomineeAddresses.length; i++) {
            nomineeArray[i] = nomineeDetails[nomineeAddresses[i]];
        }
        return nomineeArray;
    }

    // BankDetails Functions
    function addBankDetails(
        address wallet,
        string memory bankName,
        string memory accountNumber,
        string memory ifscCode
    ) public {
        require(!bankDetails[wallet]._exist, "Details Already Existed");

        BankDetails memory new_bank = BankDetails(wallet, bankName, accountNumber, ifscCode, true);
        bankDetails[wallet] = new_bank;
        bankAddresses.push(wallet);
    }

    function viewBankDetailsByWallet(address wallet) public view returns (BankDetails memory) {
        require(bankDetails[wallet]._exist, "No record with this wallet");
        return bankDetails[wallet];
    }

    function viewAllBankDetails() public view returns (BankDetails[] memory) {
        BankDetails[] memory bankArray = new BankDetails[](bankAddresses.length);

        for (uint i = 0; i < bankAddresses.length; i++) {
            bankArray[i] = bankDetails[bankAddresses[i]];
        }
        return bankArray;
    }

    // CertificateDetails Functions
    function addCertificateDetails(
        address wallet,
        string memory policyPaperPath,
        string memory policyPaperHash,
        string memory reportPaperPath,
        string memory reportPaperHash
    ) public {
        require(!certificates[wallet]._exist, "Details Already Existed");

        certificateDetails memory new_certificate = certificateDetails(
            wallet,
            policyPaperPath,
            policyPaperHash,
            reportPaperPath,
            reportPaperHash,
            true
        );
        certificates[wallet] = new_certificate;
        certificateAddresses.push(wallet);
    }

    function viewCertificateDetailsByWallet(address wallet) public view returns (certificateDetails memory) {
        require(certificates[wallet]._exist, "No record with this wallet");
        return certificates[wallet];
    }

    function viewAllCertificateDetails() public view returns (certificateDetails[] memory) {
        certificateDetails[] memory certificateArray = new certificateDetails[](certificateAddresses.length);

        for (uint i = 0; i < certificateAddresses.length; i++) {
            certificateArray[i] = certificates[certificateAddresses[i]];
        }
        return certificateArray;
    }

    function addPoliceDetails(
        address wallet,
        string memory policyId,
        string memory policeName,
        string memory policeContactNumber,
        string memory policeFIRPath,
        string memory policeFIRHash
    ) public {
        require(!policeDetails[wallet]._exist, "Details Already Existed");

        PoliceDetails memory new_police = PoliceDetails(
            wallet,
            policyId,
            policeName,
            policeContactNumber,
            policeFIRPath,
            policeFIRHash,
            true
        );
        policeDetails[wallet] = new_police;
        policeAddresses.push(wallet);
    }

    function viewPoliceDetailsByWallet(address wallet) public view returns (PoliceDetails memory) {
        require(policeDetails[wallet]._exist, "No record with this wallet");
        return policeDetails[wallet];
    }

    function viewAllPoliceDetails() public view returns (PoliceDetails[] memory) {
        PoliceDetails[] memory policeArray = new PoliceDetails[](policeAddresses.length);

        for (uint i = 0; i < policeAddresses.length; i++) {
            policeArray[i] = policeDetails[policeAddresses[i]];
        }
        return policeArray;
    }

    // HospitalDetails Functions
    function addHospitalDetails(
        address wallet,
        string memory policyId,
        string memory doctorName,
        string memory doctorContactNumber,
        string memory doctorReportPath,
        string memory doctorReportHash
    ) public {
        require(!hospitalDetails[wallet]._exist, "Details Already Existed");

        HospitalDetails memory new_hospital = HospitalDetails(
            wallet,
            policyId,
            doctorName,
            doctorContactNumber,
            doctorReportPath,
            doctorReportHash,
            true
        );
        hospitalDetails[wallet] = new_hospital;
        hospitalAddresses.push(wallet);
    }

    function viewHospitalDetailsByWallet(address wallet) public view returns (HospitalDetails memory) {
        require(hospitalDetails[wallet]._exist, "No record with this wallet");
        return hospitalDetails[wallet];
    }

    function viewAllHospitalDetails() public view returns (HospitalDetails[] memory) {
        HospitalDetails[] memory hospitalArray = new HospitalDetails[](hospitalAddresses.length);

        for (uint i = 0; i < hospitalAddresses.length; i++) {
            hospitalArray[i] = hospitalDetails[hospitalAddresses[i]];
        }
        return hospitalArray;
    }
}

